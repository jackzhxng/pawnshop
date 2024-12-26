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
	# This function would update the UI to show the items currently offered by
	# the shop. For simplicity, we just print them to the console here.
	print("Shop offers the following items:")
	for item in offered_items:
		print("- %s for %d gold" % [item["name"], item["price"]])

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
		print("Player sold %s for %d gold" % [item_name, price])
		chat_manager.provide_tool_result(id, {"success": true})
