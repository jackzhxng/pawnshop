class_name Item
extends Sprite2D

var item_spritesheet: Texture = preload("res://item_sprites/Items.png")

func init(spritesheet_coords: Vector2i):
	texture = AtlasTexture.new()
	texture.atlas = item_spritesheet
	texture.region = Rect2(spritesheet_coords * Vector2i(16, 16), Vector2i(16, 16))