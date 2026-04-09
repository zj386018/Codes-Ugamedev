extends Control

@onready var save_btn: Button = $VBox/SaveBtn
@onready var load_btn: Button = $VBox/LoadBtn
@onready var reset_btn: Button = $VBox/ResetBtn
@onready var back_btn: Button = $VBox/BackBtn
@onready var play_time_label: Label = $VBox/PlayTimeLabel
@onready var stats_label: Label = $VBox/StatsLabel


func _ready() -> void:
	save_btn.pressed.connect(_on_save)
	load_btn.pressed.connect(_on_load)
	reset_btn.pressed.connect(_on_reset)
	back_btn.pressed.connect(_on_back)
	_update_stats()


func _update_stats() -> void:
	play_time_label.text = "游戏时间: %s" % FormatUtils.format_time(GameManager.play_time)
	stats_label.text = "击杀怪物: %d\n最高伤害: %d\n总金币: %s" % [
		BattleManager.total_monsters_killed,
		BattleManager.highest_damage,
		FormatUtils.format_number(EconomyManager.total_gold_earned),
	]


func _on_save() -> void:
	SaveManager.save_game()
	NotificationManager.show_toast("存档成功!")


func _on_load() -> void:
	if SaveManager.load_game():
		NotificationManager.show_toast("读档成功!")
	else:
		NotificationManager.show_toast("没有找到存档!")


func _on_reset() -> void:
	SaveManager.delete_save()
	NotificationManager.show_toast("存档已删除! 请重启游戏。")


func _on_back() -> void:
	_update_stats()
