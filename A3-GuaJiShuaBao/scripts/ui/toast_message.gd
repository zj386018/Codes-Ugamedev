extends CanvasItem

@export var message: String = ""

var _lifetime: float = 2.5
var _elapsed: float = 0.0

@onready var label: Label = $Panel/Label


func _ready() -> void:
	label.text = message
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 1.0, 0.3).from(0.0)


func _process(delta: float) -> void:
	_elapsed += delta
	if _elapsed > _lifetime - 0.5:
		modulate.a = (_lifetime - _elapsed) / 0.5
	if _elapsed >= _lifetime:
		queue_free()
