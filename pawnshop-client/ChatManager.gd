extends Node2D

@export var send_button := Button
@export var text_input := TextEdit

var messages = []

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
	http.request("http://127.0.0.1:5000/api/chat", [], HTTPClient.METHOD_POST, json)
	messages.append("[b]You:[/b] " + message)
	refresh_text()

func run_server():
	# OS.execute('python ../server/main.py', [])
	pass


func _on_request_completed(_result, _response_code, _headers, body):
	var text = body.get_string_from_utf8()
	print("Received response: ", text)
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
			# For demo purposes, respond with a dummy inventory result.
			var result_payload = {"session_id": tc.get("session_id", "default"), "tool_call_id": tc["id"], "result": {"items": ["Ancient mushroom", "Steel dagger"]}}
			var json2 = JSON.stringify(result_payload)
			http.request("http://127.0.0.1:5000/api/tool_result", [], HTTPClient.METHOD_POST, json2)
			return
	# Fallback: append raw text
	messages.append("[b]Erik:[/b] " + text)
	refresh_text()
