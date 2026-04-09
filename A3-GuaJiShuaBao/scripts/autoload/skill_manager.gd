extends Node

signal skill_unlocked(skill_id: StringName)
signal skill_upgraded(skill_id: StringName, new_level: int)
signal active_skill_used(skill_id: StringName)

# skill_id -> level (0 = locked)
var skill_levels: Dictionary = {}
# Equipped active skill IDs (max 4)
var equipped_skills: Array[StringName] = [&"", &"", &"", &""]
# Skill definitions
var _skill_definitions: Dictionary = {}  # skill_id -> SkillResource

# Cooldown timers for active skills
var _cooldowns: Dictionary = {}  # skill_id -> remaining seconds

func _ready() -> void:
	_generate_skill_tree()


func _generate_skill_tree() -> void:
	# Active skills
	_add_skill("slash", "斩击", "基础攻击技能，造成额外伤害", Constants.SkillType.ACTIVE, 1.5, 0.2, 3.0, Constants.Stat.NONE, 0.0, 0.0, [], Vector2(0, 0))
	_add_skill("whirlwind", "旋风斩", "旋转攻击，造成大量伤害", Constants.SkillType.ACTIVE, 2.0, 0.4, 6.0, Constants.Stat.NONE, 0.0, 0.0, [&"slash"], Vector2(1, 0))
	_add_skill("power_strike", "猛击", "蓄力一击，极高伤害", Constants.SkillType.ACTIVE, 3.0, 0.6, 8.0, Constants.Stat.NONE, 0.0, 0.0, [&"slash"], Vector2(-1, 0))
	_add_skill("fire_slash", "烈焰斩", "附带火焰的强力斩击", Constants.SkillType.ACTIVE, 2.5, 0.5, 7.0, Constants.Stat.NONE, 0.0, 0.0, [&"whirlwind", &"power_strike"], Vector2(0, -1))
	_add_skill("berserk", "狂暴", "牺牲防御换取攻击力", Constants.SkillType.ACTIVE, 1.0, 0.3, 10.0, Constants.Stat.ATK, 0.2, 0.05, [&"fire_slash"], Vector2(0, -2))

	# Passive skills - Attack branch
	_add_skill("atk_boost_1", "力量I", "永久增加攻击力", Constants.SkillType.PASSIVE, 0.0, 0.0, 0.0, Constants.Stat.ATK, 3.0, 2.0, [], Vector2(2, 1))
	_add_skill("atk_boost_2", "力量II", "大幅增加攻击力", Constants.SkillType.PASSIVE, 0.0, 0.0, 0.0, Constants.Stat.ATK, 5.0, 3.0, [&"atk_boost_1"], Vector2(2, 0))
	_add_skill("crit_rate_1", "锐利I", "提升暴击率", Constants.SkillType.PASSIVE, 0.0, 0.0, 0.0, Constants.Stat.CRIT_RATE, 0.03, 0.02, [&"atk_boost_1"], Vector2(3, 1))
	_add_skill("crit_rate_2", "锐利II", "大幅提升暴击率", Constants.SkillType.PASSIVE, 0.0, 0.0, 0.0, Constants.Stat.CRIT_RATE, 0.05, 0.03, [&"crit_rate_1"], Vector2(3, 0))
	_add_skill("crit_dmg_1", "致命一击", "提升暴击伤害", Constants.SkillType.PASSIVE, 0.0, 0.0, 0.0, Constants.Stat.CRIT_DMG, 0.15, 0.1, [&"crit_rate_1"], Vector2(4, 0))

	# Passive skills - Defense branch
	_add_skill("def_boost_1", "坚韧I", "永久增加防御力", Constants.SkillType.PASSIVE, 0.0, 0.0, 0.0, Constants.Stat.DEF, 3.0, 2.0, [], Vector2(-2, 1))
	_add_skill("def_boost_2", "坚韧II", "大幅增加防御力", Constants.SkillType.PASSIVE, 0.0, 0.0, 0.0, Constants.Stat.DEF, 5.0, 3.0, [&"def_boost_1"], Vector2(-2, 0))
	_add_skill("hp_boost_1", "生命I", "永久增加生命值", Constants.SkillType.PASSIVE, 0.0, 0.0, 0.0, Constants.Stat.HP, 20.0, 15.0, [&"def_boost_1"], Vector2(-3, 1))
	_add_skill("hp_boost_2", "生命II", "大幅增加生命值", Constants.SkillType.PASSIVE, 0.0, 0.0, 0.0, Constants.Stat.HP, 40.0, 25.0, [&"hp_boost_1"], Vector2(-3, 0))
	_add_skill("spd_boost_1", "迅捷", "提升攻击速度", Constants.SkillType.PASSIVE, 0.0, 0.0, 0.0, Constants.Stat.SPD, 2.0, 1.5, [&"def_boost_1"], Vector2(-3, -1))

	# Initialize all skills to level 0 (locked)
	for skill_id in _skill_definitions:
		skill_levels[skill_id] = 0


func _add_skill(id: String, skill_name: String, desc: String, type: int, dmg_base: float, dmg_per_lvl: float, cd: float, stat: int, passive_base: float, passive_per_lvl: float, prereqs: Array, pos: Vector2) -> void:
	var skill := SkillResource.new()
	skill.id = StringName(id)
	skill.name = skill_name
	skill.description = desc
	skill.skill_type = type
	skill.damage_multiplier_base = dmg_base
	skill.damage_multiplier_per_level = dmg_per_lvl
	skill.cooldown_seconds = cd
	skill.passive_stat = stat
	skill.passive_bonus_base = passive_base
	skill.passive_bonus_per_level = passive_per_lvl
	skill.prerequisites = prereqs
	skill.grid_position = pos
	_skill_definitions[StringName(id)] = skill


func can_unlock_or_upgrade(skill_id: StringName) -> bool:
	var skill: SkillResource = _skill_definitions.get(skill_id)
	if skill == null:
		return false
	var current_level = skill_levels.get(skill_id, 0)
	# Check max level
	if current_level >= skill.max_level:
		return false
	# Check prerequisites
	for prereq in skill.prerequisites:
		if skill_levels.get(prereq, 0) <= 0:
			return false
	# Check skill points
	if PlayerData.skill_points_available <= 0:
		return false
	return true


func upgrade_skill(skill_id: StringName) -> void:
	if not can_unlock_or_upgrade(skill_id):
		return
	var skill: SkillResource = _skill_definitions[skill_id]
	var current_level = skill_levels.get(skill_id, 0)
	PlayerData.skill_points_available -= 1
	skill_levels[skill_id] = current_level + 1

	if current_level == 0:
		skill_unlocked.emit(skill_id)
	else:
		skill_upgraded.emit(skill_id, current_level + 1)

	_apply_passive_bonuses()


func equip_active_skill(skill_id: StringName, slot_index: int) -> void:
	if slot_index < 0 or slot_index >= Constants.MAX_EQUIPPED_SKILLS:
		return
	if skill_levels.get(skill_id, 0) <= 0:
		return
	var skill: SkillResource = _skill_definitions[skill_id]
	if skill.skill_type != Constants.SkillType.ACTIVE:
		return
	# Remove from other slot if already equipped
	for i in Constants.MAX_EQUIPPED_SKILLS:
		if equipped_skills[i] == skill_id:
			equipped_skills[i] = &""
	equipped_skills[slot_index] = skill_id


func get_ready_skill() -> StringName:
	# Find the first equipped skill that's off cooldown
	for skill_id in equipped_skills:
		if skill_id != &"" and _cooldowns.get(skill_id, 0.0) <= 0.0:
			var level = skill_levels.get(skill_id, 0)
			if level > 0:
				return skill_id
	return &""


func use_skill(skill_id: StringName) -> void:
	var skill: SkillResource = _skill_definitions.get(skill_id)
	if skill == null:
		return
	_cooldowns[skill_id] = skill.cooldown_seconds
	active_skill_used.emit(skill_id)


func tick_cooldowns(delta: float) -> void:
	for skill_id in _cooldowns:
		_cooldowns[skill_id] = maxf(0.0, _cooldowns[skill_id] - delta)


func get_skill_definition(skill_id: StringName) -> SkillResource:
	return _skill_definitions.get(skill_id)


func get_all_definitions() -> Dictionary:
	return _skill_definitions


func _apply_passive_bonuses() -> void:
	PlayerData.skill_bonus_hp = 0
	PlayerData.skill_bonus_atk = 0
	PlayerData.skill_bonus_def = 0
	PlayerData.skill_bonus_spd = 0
	PlayerData.skill_bonus_crit_rate = 0.0
	PlayerData.skill_bonus_crit_dmg = 0.0

	for skill_id in skill_levels:
		var level: int = skill_levels[skill_id]
		if level <= 0:
			continue
		var skill: SkillResource = _skill_definitions[skill_id]
		if skill.skill_type != Constants.SkillType.PASSIVE:
			continue
		var bonus = skill.get_passive_bonus(level)
		match skill.passive_stat:
			Constants.Stat.HP: PlayerData.skill_bonus_hp += int(bonus)
			Constants.Stat.ATK: PlayerData.skill_bonus_atk += int(bonus)
			Constants.Stat.DEF: PlayerData.skill_bonus_def += int(bonus)
			Constants.Stat.SPD: PlayerData.skill_bonus_spd += int(bonus)
			Constants.Stat.CRIT_RATE: PlayerData.skill_bonus_crit_rate += bonus
			Constants.Stat.CRIT_DMG: PlayerData.skill_bonus_crit_dmg += bonus

	PlayerData.notify_stats_changed()


func serialize() -> Dictionary:
	var skills_data = {}
	for skill_id in skill_levels:
		skills_data[String(skill_id)] = skill_levels[skill_id]
	return {
		"skills": skills_data,
		"equipped": equipped_skills.map(func(s): return String(s)),
	}


func deserialize(data: Dictionary) -> void:
	skill_levels.clear()
	var skills_data = data.get("skills", {})
	for skill_key in skills_data:
		skill_levels[StringName(skill_key)] = skills_data[skill_key]

	equipped_skills.clear()
	var eq_data = data.get("equipped", [&"", &"", &"", &""])
	for i in mini(eq_data.size(), 4):
		equipped_skills.append(StringName(eq_data[i]))

	_apply_passive_bonuses()
