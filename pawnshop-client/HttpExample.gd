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
	http.request("http://127.0.0.1:8080/chat?message=" + message.uri_encode(), [], HTTPClient.METHOD_GET)
	messages.append("[b]You:[/b] " + message)
	refresh_text()

func run_server():
	# OS.execute('python ../server/main.py', [])
	pass


func _on_request_completed(_result, _response_code, _headers, body):
	# var json = JSON.parse_string(body.get_string_from_utf8())
	var output = body.get_string_from_utf8()
	messages.append("[b]Erik:[/b] " + output)
	refresh_text()
