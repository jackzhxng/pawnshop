class_name Inventory
extends Node2D

@export var chat_manager: ChatManager

var item_data := preload("res://item_data.json")
var inventory_items_json := ""

func _ready():
	randomize()
	generate_random_inventory()
	chat_manager.tool_call_received.connect(handle_tool_call_received)

func generate_random_inventory():
	# Load and parse the source item data JSON file
	var file := FileAccess.open("res://item_data.json", FileAccess.READ)
	if file == null:
		push_error("Failed to open item_data.json")
		inventory_items_json = "[]"
		return

	var json_text := file.get_as_text()
	file.close()

	var parsed = JSON.parse_string(json_text)
	if typeof(parsed) != TYPE_ARRAY:
		push_error("item_data.json must contain a top-level array")
		inventory_items_json = "[]"
		return

	var items: Array = parsed
	if items.is_empty():
		inventory_items_json = "[]"
		return

	# Pick up to 3 unique random items
	var count = min(3, items.size())
	var pool := items.duplicate(true)
	pool.shuffle()
	var selection: Array = []
	for i in range(count):
		selection.append(pool[i])

	# Store as a JSON array string
	inventory_items_json = JSON.stringify(selection)
	# Optional: print for debugging
	print("Inventory items:", inventory_items_json)

func handle_tool_call_received(tool_name, args, id):
	if tool_name == "get_inventory":
		print("Got tool call for inventory with id: ", id)
		# Respond with the current inventory items JSON string
		chat_manager.provide_tool_result(id, inventory_items_json)
		print("Provided inventory result: ", inventory_items_json)
