@tool
class_name Item
extends Sprite2D

@export var item_name := "Iron Shortsword"
var item_spritesheet: Texture = preload("res://item_sprites/Items.png")

@export_tool_button("Initialize Item", "Callable") var init_action = init

func init_sprite(spritesheet_coords: Vector2i):
	texture = AtlasTexture.new()
	texture.atlas = item_spritesheet
	texture.region = Rect2(spritesheet_coords * Vector2i(16, 16), Vector2i(16, 16))

func init():
	var coords = ItemSpriteRegistry.registry.get(item_name, null)
	if coords != null:
		init_sprite(coords)
	else:
		print("Item '%s' not found in registry." % item_name)
		texture = null