extends Control

@onready var time_label: Label = $Panel/VBox/TimeLabel
@onready var gold_label: Label = $Panel/VBox/GoldLabel
@onready var xp_label: Label = $Panel/VBox/XPLabel
@onready var collect_btn: Button = $Panel/VBox/CollectBtn

var _rewards: Dictionary = {}

func _ready() -> void:
	collect_btn.pressed.connect(_on_collect)


func setup(rewards: Dictionary) -> void:
	_rewards = rewards
	var hours = rewards.get("seconds", 0.0) / 3600.0
	time_label.text = "离线时间: %.1f小时" % hours
	gold_label.text = "获得金币: %s" % FormatUtils.format_number(rewards.get("gold", 0))
	xp_label.text = "获得经验: %s" % FormatUtils.format_number(rewards.get("xp", 0))


func _on_collect() -> void:
	var gold = _rewards.get("gold", 0)
	var xp = _rewards.get("xp", 0)
	if gold > 0:
		EconomyManager.add_gold(gold)
	if xp > 0:
		PlayerData.add_experience(xp)
	queue_free()
