extends Node2D

@export var send_button := Button
@export var text_input := TextEdit

var messages = []

signal tool_call_received(name, args, id)

var pending_tool_call_id = null

@onready var http = %HTTPRequest
@onready var chat_text = %Text

func _ready():
	http.request_completed.connect(_on_request_completed)
	send_button.pressed.connect(on_button_pressed)
	chat_text.scroll_following = true
	
func refresh_text():
	chat_text.text = ""
	for message in messages:
		chat_text.text += message + "\n\n"

func on_button_pressed():
	var message = text_input.text
	var payload = {"message": message}
	var json = JSON.stringify(payload)
	http.request("http://127.0.0.1:8080/api/chat", [], HTTPClient.METHOD_POST, json)
	messages.append("[b]You:[/b] " + message)
	refresh_text()
	text_input.text = ""

func run_server():
	# OS.execute('python ../server/main.py', [])
	pass


func _on_request_completed(_result, _response_code, _headers, body):
	var text = body.get_string_from_utf8()
	print("Received response: ", text)
	# If server returned 404 for a tool_result post, show TTL/expired UX
	if _response_code == 404 and pending_tool_call_id != null:
		messages.append("[b]System:[/b] Tool call expired or not found on server.")
		pending_tool_call_id = null
		refresh_text()
		return
	var json = JSON.new()
	var error = json.parse(text)
	if error == OK:
		var obj = json.data
		if obj.has("status") and obj["status"] == "finished":
			messages.append("[b]Erik:[/b] " + obj["reply"])
			refresh_text()
			return
		elif obj.has("status") and obj["status"] == "tool_call":
			var tc = obj["tool_call"]
			# Delegate tool execution to local handler which will emit a signal
			# and wait for an explicit provide_tool_result call from scene nodes.
			handle_tool_call(tc["name"].to_lower(), tc.get("args", {}), tc["id"])
			return
		# If a previous tool_result post returned 404 (expired/TTL), show notice
		if _response_code == 404 and pending_tool_call_id != null:
			messages.append("[b]System:[/b] Tool call expired or not found on server.")
			pending_tool_call_id = null
			refresh_text()
			return
	# Fallback: append raw text
	messages.append("[b]Erik:[/b] " + text)
	refresh_text()


func handle_tool_call(tool_name, args, id):
	# Emit signal so scene nodes (inventory UI, animations) can react and
	# supply results asynchronously by calling `provide_tool_result`.
	emit_signal("tool_call_received", tool_name, args, id)

	# Mark this call as pending; UI should collect result and call
	# `provide_tool_result(id, result)` when ready.
	pending_tool_call_id = id
	messages.append("[b]System:[/b] Tool call received: %s — waiting for client result..." % tool_name)
	refresh_text()


func provide_tool_result(tool_call_id, result):
	# Called by scene nodes when they have the concrete result for a tool call.
	if pending_tool_call_id == null:
		messages.append("[b]System:[/b] No pending tool call to provide results for.")
		refresh_text()
		return
	if str(tool_call_id) != str(pending_tool_call_id):
		messages.append("[b]System:[/b] Tool call id mismatch.")
		refresh_text()
		return

	var payload = {"tool_call_id": tool_call_id, "result": result}
	var json2 = JSON.stringify(payload)

	# Post the result back to the server; server will resume the agent and
	# respond with the next assistant message which will be handled in
	# _on_request_completed.
	http.request("http://127.0.0.1:8080/api/tool_result", [], HTTPClient.METHOD_POST, json2)

	# Keep pending_tool_call_id until server confirms; TTL/404 handling will
	# clear it if expired.
