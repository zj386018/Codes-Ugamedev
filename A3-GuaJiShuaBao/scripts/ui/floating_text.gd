extends Node2D

@export var display_text: String = ""
@export var text_color: Color = Color.WHITE
@export var is_crit: bool = false

var _lifetime: float = 1.0
var _elapsed: float = 0.0
var _velocity: Vector2 = Vector2.UP * 80

@onready var label: Label = $Label


func _ready() -> void:
	label.text = display_text
	label.add_theme_color_override("font_color", text_color)
	if is_crit:
		label.add_theme_font_size_override("font_size", 28)
		label.add_theme_color_override("font_color", Color.YELLOW)
	else:
		label.add_theme_font_size_override("font_size", 20)


func _process(delta: float) -> void:
	_elapsed += delta
	position += _velocity * delta
	_velocity.y -= 20 * delta  # Slow down upward movement

	# Fade out in last 0.3 seconds
	if _elapsed > _lifetime - 0.3:
		modulate.a = (_lifetime - _elapsed) / 0.3

	if _elapsed >= _lifetime:
		queue_free()


static func create(parent: Node, pos: Vector2, text: String, color: Color, crit: bool = false) -> void:
	var scene = preload("res://scenes/battle/floating_text.tscn")
	var instance = scene.instantiate()
	instance.display_text = text
	instance.text_color = color
	instance.is_crit = crit
	instance.position = pos
	parent.add_child(instance)
