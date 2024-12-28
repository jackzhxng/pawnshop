@tool
class_name Item
extends Sprite2D

@export var item_name := "Iron Shortsword"
@export var item_price := 100
var item_spritesheet: Texture = preload("res://item_sprites/Items.png")

@export_tool_button("Initialize Item", "Callable") var init_action = init

func init_sprite(spritesheet_coords: Vector2i):
	texture = AtlasTexture.new()
	texture.atlas = item_spritesheet
	texture.region = Rect2(spritesheet_coords * Vector2i(16, 16), Vector2i(16, 16))

	var price_label = Label.new()
	price_label.text = str(item_price) + "g"
	price_label.position = Vector2(0, 20)
	price_label.anchor_left = 0.5
	price_label.anchor_right = 0.5
	price_label.anchor_top = 0.5
	price_label.anchor_bottom = 0.5
	price_label.offset_left = -28
	price_label.offset_right = 12
	price_label.offset_top = -40
	price_label.offset_bottom = 4
	add_child(price_label)

func init():
	var coords = ItemSpriteRegistry.registry.get(item_name, null)
	if coords != null:
		init_sprite(coords)
	else:
		print("Item '%s' not found in registry." % item_name)
		texture = null