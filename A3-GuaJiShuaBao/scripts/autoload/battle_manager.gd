extends Node

signal player_attacked(damage: int, is_crit: bool)
signal monster_attacked(damage: int, is_crit: bool)
signal monster_died(monster: MonsterResource, gold: int, xp: int)
signal player_died
signal stage_completed(stage_number: int)
signal boss_defeated(stage_number: int)
signal skill_fired(skill_name: String)

var _battle_timer: float = 0.0
var _is_active: bool = false
var _player_dead: bool = false
var _retry_timer: float = 0.0

# Current monster state
var current_monster: MonsterResource
var monster_hp: int = 0
var monster_max_hp: int = 0
var monster_atk: int = 0
var monster_def: int = 0
var monster_spd: int = 0

# Stats
var total_monsters_killed: int = 0
var highest_damage: int = 0


func _ready() -> void:
	PlayerData.stats_changed.connect(_on_player_stats_changed)
	StageManager.stage_changed.connect(_on_stage_changed)


func start_battle() -> void:
	_is_active = true
	_player_dead = false
	PlayerData.full_heal()
	_spawn_monster()


func stop_battle() -> void:
	_is_active = false


func _process(delta: float) -> void:
	if not _is_active:
		return

	if _player_dead:
		_retry_timer -= delta
		if _retry_timer <= 0:
			_player_dead = false
			PlayerData.full_heal()
			_spawn_monster()
		return

	# Tick skill cooldowns
	SkillManager.tick_cooldowns(delta)

	# Battle tick
	_battle_timer += delta
	if _battle_timer >= Constants.BATTLE_TICK_RATE:
		_battle_timer -= Constants.BATTLE_TICK_RATE
		_execute_combat_round()


func _execute_combat_round() -> void:
	var player_atk = PlayerData.get_total_atk()
	var player_def = PlayerData.get_total_def()
	var player_spd = PlayerData.get_total_spd()
	var player_crit_rate = PlayerData.get_total_crit_rate()
	var player_crit_dmg = PlayerData.get_total_crit_dmg()
	var player_hp = PlayerData.current_hp

	# Check for active skill
	var skill_id = SkillManager.get_ready_skill()
	var skill_multiplier = 1.0
	if skill_id != &"":
		var skill: SkillResource = SkillManager.get_skill_definition(skill_id)
		var level = SkillManager.skill_levels.get(skill_id, 0)
		skill_multiplier = skill.get_damage_multiplier(level)
		SkillManager.use_skill(skill_id)
		skill_fired.emit(skill.name)

	# Determine turn order by speed
	if player_spd >= monster_spd:
		_player_attacks(player_atk, player_crit_rate, player_crit_dmg, skill_multiplier)
		if monster_hp > 0:
			_monster_attacks(monster_atk, player_def)
	else:
		_monster_attacks(monster_atk, player_def)
		if PlayerData.current_hp > 0:
			_player_attacks(player_atk, player_crit_rate, player_crit_dmg, skill_multiplier)


func _player_attacks(atk: int, crit_rate: float, crit_dmg: float, skill_mult: float) -> void:
	var result = DamageCalculator.compute_damage(atk, monster_def, crit_rate, crit_dmg, skill_mult)
	monster_hp = maxi(0, monster_hp - result.damage)
	if result.damage > highest_damage:
		highest_damage = result.damage
	player_attacked.emit(result.damage, result.is_crit)

	if monster_hp <= 0:
		_on_monster_killed()


func _monster_attacks(atk: int, player_def: int) -> void:
	var result = DamageCalculator.compute_damage(atk, player_def, 0.05, 1.3)
	PlayerData.take_damage(result.damage)
	monster_attacked.emit(result.damage, result.is_crit)

	if PlayerData.current_hp <= 0:
		_on_player_died()


func _on_monster_killed() -> void:
	var gold = current_monster.get_gold_drop()
	var stage = StageManager.current_stage
	# Apply stage multiplier - gold scales with stage
	gold = int(gold * (1.0 + (stage - 1) * 0.1))
	var xp = int(current_monster.xp_reward * (1.0 + (stage - 1) * 0.05))

	EconomyManager.add_gold(gold)
	PlayerData.add_experience(xp)
	EquipmentManager.roll_loot(stage)
	total_monsters_killed += 1

	monster_died.emit(current_monster, gold, xp)
	StageManager.on_monster_killed()

	# Check if stage is complete
	if StageManager.should_advance_stage():
		var completed_stage = StageManager.current_stage
		if StageManager.is_boss_stage(completed_stage):
			StageManager.on_boss_defeated(completed_stage)
			boss_defeated.emit(completed_stage)
		stage_completed.emit(completed_stage)
		StageManager.advance_to_next_stage()
	else:
		_spawn_monster()


func _on_player_died() -> void:
	_player_dead = true
	_retry_timer = 3.0
	player_died.emit()


func _spawn_monster() -> void:
	var stage = StageManager.current_stage
	if StageManager.is_boss_stage(stage):
		current_monster = StageManager.get_boss_for_stage(stage)
	else:
		current_monster = StageManager.get_monster_for_stage(stage)

	monster_hp = current_monster.get_scaled_hp(stage)
	monster_max_hp = monster_hp
	monster_atk = current_monster.get_scaled_atk(stage)
	monster_def = current_monster.get_scaled_def(stage)
	monster_spd = current_monster.get_scaled_spd(stage)


func _on_player_stats_changed() -> void:
	# If player stats changed (e.g., equipped item), ensure HP doesn't exceed max
	if PlayerData.current_hp > PlayerData.get_total_hp():
		PlayerData.current_hp = PlayerData.get_total_hp()


func _on_stage_changed(_new_stage: int) -> void:
	_spawn_monster()


func serialize() -> Dictionary:
	return {
		"total_monsters_killed": total_monsters_killed,
		"highest_damage": highest_damage,
	}


func deserialize(data: Dictionary) -> void:
	total_monsters_killed = data.get("total_monsters_killed", 0)
	highest_damage = data.get("highest_damage", 0)
