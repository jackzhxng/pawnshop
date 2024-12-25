extends Control


# Sprite naming is as follows: "Masculine_A_default.png
# Format is "{CharacterType}_{CharacterVariation}_{Expression}.png"
@export var character_type = "Masculine"
@export var expression = "default"
@export var character_variation = "A"

# Sprite naming for hair is as follows: "Hair_A_Masculine_B-base.png
# Format is "Hair_{HairVariation}_{CharacterType}_{CharacterVariation}-base.png"
@export var hair_variation = "A"

# Sprite naming for beard is as follows: "Beard_A_Masculine_B-base.png
# Format is "Beard_{BeardVariation}_{CharacterType}_A-base.png"

@onready var character_image: TextureRect = $CharacterImage
@onready var hair_image: TextureRect = $HairImage
@onready var beard_image: TextureRect = $BeardImage

func _ready():
	update_portrait()

func update_portrait():
	var character_sprite_path = "res://character_sprites/%s_%s_%s.png" % [character_type, character_variation, expression]
	character_image.texture = load(character_sprite_path)

	var hair_sprite_path = "res://character_sprites/Hair_%s_%s_%s-base.png" % [hair_variation, character_type, character_variation]
	hair_image.texture = load(hair_sprite_path)
	
	var beard_sprite_path = "res://character_sprites/Beard_%s_%s_%s-base.png" % [hair_variation, character_type, character_variation]
	beard_image.texture = load(beard_sprite_path)

func change_expression(new_expression):
	expression = new_expression
	update_portrait()