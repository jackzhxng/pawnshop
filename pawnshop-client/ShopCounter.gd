class_name ShopCounter
extends Node2D

@export var chat_manager: ChatManager
var offered_items = []

func _ready():
	chat_manager.tool_call_received.connect(handle_tool_call_received)

	# For demo purposes, we hardcode some offered items. In a real game, these
	# would likely be loaded from a file or generated dynamically.
	# offered_items = [
	# 	{"name": "Iron Shortsword", "price": 100},
	# 	{"name": "Health Potion", "price": 50},
	# 	{"name": "Treasure Map", "price": 200},
	# ]

func display_offered_items():
	# Remove previously displayed Item nodes so we don't duplicate on repeated calls
	for child in get_children():
		child.queue_free()

	var center_x = 590
	var spacing = 100
	for i in offered_items.size():
		var item = offered_items[i]
		var x_pos = center_x
		if i == 0:
			x_pos = center_x
		else:
			var n = int((i + 1) / 2)
			if i % 2 == 1:
				x_pos = center_x + n * spacing
			else:
				x_pos = center_x - n * spacing

		var item_node = Item.new()
		item_node.position = Vector2(x_pos, 170)
		item_node.scale = Vector2(4, 4)
		item_node.item_name = item["name"]
		add_child(item_node)
		item_node.init()

func handle_tool_call_received(tool_name, args, id):
	if tool_name == "offer_item":
		var item_name = args.get("item_name", "")
		var price = args.get("price", 0)
		if item_name == "" or price <= 0:
			chat_manager.provide_tool_result(id, {"success": false, "error": "Invalid item name or price"})
			return
		
		offered_items.append({"name": item_name, "price": price})
		display_offered_items()
		chat_manager.provide_tool_result(id, {"success": true})
	
	if tool_name == "sell":
		var item_name = args.get("item", "")
		var price = args.get("price", 0)
		if offered_items.all(func(item): return item["name"] != item_name):
			chat_manager.provide_tool_result(id, {"success": false, "error": "Can't sell an item that was not offered"})
			print("Attempted to sell an item that was not offered: %s" % item_name)
			print("Current offered items: %s" % offered_items)
			return
		if item_name == "" or price <= 0:
			chat_manager.provide_tool_result(id, {"success": false, "error": "Invalid item name or price"})
			return
		
		# In a real game, you'd also want to check if the item is actually offered
		# and handle inventory updates, gold transactions, etc.
		# Remove the sold item from the offered_items list and update display
		var removed = false
		# Try to remove by matching both name and price first
		for i in offered_items.size():
			var it = offered_items[i]
			if it["name"] == item_name:
				offered_items.remove_at(i)
				removed = true
				break

		if removed:
			display_offered_items()
			print("Player sold %s for %d gold" % [item_name, price])
			chat_manager.provide_tool_result(id, {"success": true})
		else:
			# Shouldn't happen because we validated existence earlier, but handle just in case
			chat_manager.provide_tool_result(id, {"success": false, "error": "Failed to remove offered item"})
