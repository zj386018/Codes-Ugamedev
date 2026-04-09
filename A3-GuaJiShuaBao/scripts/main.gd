extends Control


func _ready() -> void:
	# The BattleScene is a Node2D child positioned in the upper portion
	var battle = $BattleScene
	battle.position = Vector2(360, 350)
