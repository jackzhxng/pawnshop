class_name ShopCounter
extends Node2D

@export var chat_manager: ChatManager
var offered_items = []
@export var player_gold := 1000
var _gold_label: Label

func _ready():
	chat_manager.tool_call_received.connect(handle_tool_call_received)

	# Create a simple gold counter label and add to the counter node
	_gold_label = Label.new()
	_gold_label.name = "GoldLabel"
	_gold_label.position = Vector2(20, 20)
	_gold_label.anchor_left = 0
	_gold_label.anchor_top = 0
	update_gold_display()
	add_child(_gold_label)

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
		# Only remove Item nodes so UI elements like the gold label are preserved
		if child is Item:
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
		item_node.item_price = item["price"]
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
		var quantity = args.get("quantity", 1)
		if offered_items.all(func(item): return item["name"] != item_name):
			chat_manager.provide_tool_result(id, {"success": false, "error": "Can't sell an item that was not offered"})
			print("Attempted to sell an item that was not offered: %s" % item_name)
			print("Current offered items: %s" % offered_items)
			return
		if item_name == "" or price <= 0 or quantity <= 0:
			chat_manager.provide_tool_result(id, {"success": false, "error": "Invalid item name, price, or quantity"})
			return

		# Total cost to the player
		var total_cost = price * quantity
		if player_gold < total_cost:
			chat_manager.provide_tool_result(id, {"success": false, "error": "Not enough gold"})
			print("Player tried to buy %s x%d for %d gold but only has %d" % [item_name, quantity, total_cost, player_gold])
			return

		# Deduct gold from the player
		player_gold -= total_cost
		update_gold_display()

		# Remove sold item(s) from the offered_items list and update display
		var removed = false
		for i in offered_items.size():
			var it = offered_items[i]
			if it["name"] == item_name:
				offered_items.remove_at(i)
				removed = true
				break

		if removed:
			display_offered_items()
			print("Player bought %s x%d for %d gold" % [item_name, quantity, total_cost])
			chat_manager.provide_tool_result(id, {"success": true, "gold_left": player_gold})
		else:
			# Shouldn't happen because we validated existence earlier, but handle just in case
			chat_manager.provide_tool_result(id, {"success": false, "error": "Failed to remove offered item"})

func update_gold_display():
	if _gold_label != null:
		_gold_label.text = str(player_gold) + "g"
