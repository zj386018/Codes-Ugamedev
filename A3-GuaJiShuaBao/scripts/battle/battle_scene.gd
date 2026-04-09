extends Node2D

@onready var player_unit: Node2D = $PlayerUnit
@onready var monster_unit: Node2D = $MonsterUnit
@onready var floating_texts: Node2D = $FloatingTexts
@onready var battle_info: Label = $BattleInfo
@onready var background: ColorRect = $Background

func _ready() -> void:
	BattleManager.player_attacked.connect(_on_player_attacked)
	BattleManager.monster_attacked.connect(_on_monster_attacked)
	BattleManager.monster_died.connect(_on_monster_died)
	BattleManager.player_died.connect(_on_player_died)
	BattleManager.stage_completed.connect(_on_stage_completed)
	BattleManager.boss_defeated.connect(_on_boss_defeated)
	BattleManager.skill_fired.connect(_on_skill_fired)
	PlayerData.hp_changed.connect(_on_player_hp_changed)
	StageManager.stage_changed.connect(_on_stage_changed)

	# Initial setup
	_setup_player()
	_setup_monster()


func _setup_player() -> void:
	player_unit.is_player = true
	player_unit._setup_player()
	player_unit.update_hp(PlayerData.current_hp, PlayerData.get_total_hp())


func _setup_monster() -> void:
	var monster = BattleManager.current_monster
	if monster == null:
		return
	monster_unit.is_player = false
	monster_unit.setup_monster(monster)
	monster_unit.update_hp(BattleManager.monster_hp, BattleManager.monster_max_hp)
	monster_unit.play_spawn()

	# Update background color based on stage
	var stage = StageManager.current_stage
	if StageManager.is_boss_stage(stage):
		background.color = Color(0.25, 0.08, 0.08)
		battle_info.text = "BOSS战! - %s" % monster.display_name
		battle_info.add_theme_color_override("font_color", Color.RED)
	else:
		background.color = Color(0.12, 0.12, 0.18)
		battle_info.text = "关卡 %d - %s" % [stage, monster.display_name]
		battle_info.add_theme_color_override("font_color", Color.WHITE)


func _on_player_attacked(damage: int, is_crit: bool) -> void:
	monster_unit.update_hp(BattleManager.monster_hp, BattleManager.monster_max_hp)
	player_unit.play_attack()
	monster_unit.play_hurt()
	_spawn_damage_text(monster_unit.position, damage, is_crit, Color(1.0, 0.9, 0.3))


func _on_monster_attacked(damage: int, is_crit: bool) -> void:
	player_unit.update_hp(PlayerData.current_hp, PlayerData.get_total_hp())
	monster_unit.play_attack()
	player_unit.play_hurt()
	_spawn_damage_text(player_unit.position, damage, is_crit, Color(1.0, 0.3, 0.3))


func _on_player_hp_changed(current: int, maximum: int) -> void:
	player_unit.update_hp(current, maximum)


func _on_monster_died(_monster: MonsterResource, gold: int, xp: int) -> void:
	monster_unit.play_death()
	# Show gold/XP gain text
	var gold_text_scene = preload("res://scenes/battle/floating_text.tscn")
	var gold_instance = gold_text_scene.instantiate()
	gold_instance.display_text = "+%d金 +%d经验" % [gold, xp]
	gold_instance.text_color = Color(0.9, 0.85, 0.2)
	gold_instance.is_crit = false
	gold_instance.position = monster_unit.position + Vector2(0, -60)
	floating_texts.add_child(gold_instance)


func _on_player_died() -> void:
	player_unit.play_death()
	battle_info.text = "战败! 3秒后重试..."
	battle_info.add_theme_color_override("font_color", Color.RED)


func _on_stage_completed(stage_number: int) -> void:
	battle_info.text = "关卡 %d 通过!" % stage_number
	battle_info.add_theme_color_override("font_color", Color.GREEN)
	var tween = create_tween()
	tween.tween_callback(func(): battle_info.text = "战斗中...").set_delay(2.0)


func _on_boss_defeated(stage_number: int) -> void:
	battle_info.text = "BOSS击败! 关卡 %d 通过!" % stage_number
	battle_info.add_theme_color_override("font_color", Color.GOLD)
	var tween = create_tween()
	tween.tween_callback(func(): battle_info.text = "战斗中...").set_delay(3.0)


func _on_skill_fired(skill_name: String) -> void:
	# Show skill name
	var skill_text = preload("res://scenes/battle/floating_text.tscn").instantiate()
	skill_text.display_text = skill_name
	skill_text.text_color = Color(0.3, 0.7, 1.0)
	skill_text.is_crit = false
	skill_text.position = player_unit.position + Vector2(0, -80)
	floating_texts.add_child(skill_text)


func _on_stage_changed(_new_stage: int) -> void:
	_setup_monster()


func _spawn_damage_text(pos: Vector2, damage: int, is_crit: bool, color: Color) -> void:
	var instance = preload("res://scenes/battle/floating_text.tscn").instantiate()
	instance.display_text = str(damage)
	instance.text_color = color
	instance.is_crit = is_crit
	instance.position = pos + Vector2(randf_range(-20, 20), -40)
	floating_texts.add_child(instance)
