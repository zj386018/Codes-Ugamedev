extends Control

@onready var level_label: Label = $VBox/LevelLabel
@onready var hp_label: Label = $VBox/StatsContainer/HPLabel
@onready var atk_label: Label = $VBox/StatsContainer/ATKLabel
@onready var def_label: Label = $VBox/StatsContainer/DEFLabel
@onready var spd_label: Label = $VBox/StatsContainer/SPDLabel
@onready var crit_rate_label: Label = $VBox/StatsContainer/CritRateLabel
@onready var crit_dmg_label: Label = $VBox/StatsContainer/CritDmgLabel
@onready var points_label: Label = $VBox/PointsContainer/PointsLabel
@onready var hp_btn: Button = $VBox/PointsContainer/HBox/HPBtn
@onready var atk_btn: Button = $VBox/PointsContainer/HBox/ATKBtn
@onready var def_btn: Button = $VBox/PointsContainer/HBox/DEFBtn
@onready var spd_btn: Button = $VBox/PointsContainer/HBox/SPDBtn


func _ready() -> void:
	PlayerData.stats_changed.connect(_update_display)
	PlayerData.hp_changed.connect(_on_hp_changed)
	hp_btn.pressed.connect(func(): PlayerData.allocate_stat(Constants.Stat.HP))
	atk_btn.pressed.connect(func(): PlayerData.allocate_stat(Constants.Stat.ATK))
	def_btn.pressed.connect(func(): PlayerData.allocate_stat(Constants.Stat.DEF))
	spd_btn.pressed.connect(func(): PlayerData.allocate_stat(Constants.Stat.SPD))
	_update_display()


func _update_display() -> void:
	level_label.text = "等级: %d" % PlayerData.level
	hp_label.text = "生命: %d" % PlayerData.get_total_hp()
	atk_label.text = "攻击: %d" % PlayerData.get_total_atk()
	def_label.text = "防御: %d" % PlayerData.get_total_def()
	spd_label.text = "速度: %d" % PlayerData.get_total_spd()
	crit_rate_label.text = "暴击率: %.1f%%" % (PlayerData.get_total_crit_rate() * 100)
	crit_dmg_label.text = "暴击伤害: %.1fx" % PlayerData.get_total_crit_dmg()
	points_label.text = "可用点数: %d" % PlayerData.stat_points_available

	var has_points = PlayerData.stat_points_available > 0
	hp_btn.disabled = not has_points
	atk_btn.disabled = not has_points
	def_btn.disabled = not has_points
	spd_btn.disabled = not has_points


func _on_hp_changed(_current: int, _maximum: int) -> void:
	_update_display()
