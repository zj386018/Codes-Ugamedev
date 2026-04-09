extends HBoxContainer

@onready var gold_label: Label = $GoldLabel
@onready var level_label: Label = $LevelLabel
@onready var stage_label: Label = $StageLabel
@onready var monsters_label: Label = $MonstersLabel
@onready var xp_bar: ProgressBar = $"../XPBar"
@onready var xp_label: Label = $"../XPBar/XPLabel"


func _ready() -> void:
	EconomyManager.gold_changed.connect(_on_gold_changed)
	PlayerData.level_up.connect(_on_level_up)
	PlayerData.experience_gained.connect(_on_xp_gained)
	StageManager.stage_changed.connect(_on_stage_changed)
	StageManager.stage_unlocked.connect(_on_stage_unlocked)
	BattleManager.monster_died.connect(_on_monster_died)
	_update_display()


func _update_display() -> void:
	gold_label.text = "金币: %s" % FormatUtils.format_number(EconomyManager.gold)
	level_label.text = "Lv.%d" % PlayerData.level
	stage_label.text = "关卡 %d" % StageManager.current_stage
	_update_xp_bar()
	_update_monsters_label()


func _update_xp_bar() -> void:
	xp_bar.max_value = PlayerData.experience_to_next
	xp_bar.value = PlayerData.experience
	xp_label.text = "%s / %s" % [FormatUtils.format_number(PlayerData.experience), FormatUtils.format_number(PlayerData.experience_to_next)]


func _update_monsters_label() -> void:
	var killed = StageManager.monsters_killed_this_stage
	var total = StageManager.get_monster_count(StageManager.current_stage)
	monsters_label.text = "怪物: %d/%d" % [killed, total]


func _on_gold_changed(new_amount: int, _delta: int) -> void:
	gold_label.text = "金币: %s" % FormatUtils.format_number(new_amount)


func _on_level_up(new_level: int) -> void:
	level_label.text = "Lv.%d" % new_level


func _on_xp_gained(_amount: int, _total: int, _needed: int) -> void:
	_update_xp_bar()


func _on_stage_changed(_new_stage: int) -> void:
	stage_label.text = "关卡 %d" % StageManager.current_stage
	_update_monsters_label()


func _on_stage_unlocked(_stage: int) -> void:
	_update_monsters_label()


func _on_monster_died(_monster: MonsterResource, _gold: int, _xp: int) -> void:
	_update_monsters_label()
