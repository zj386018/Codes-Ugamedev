extends Node

signal stats_changed
signal level_up(new_level: int)
signal experience_gained(amount: int, total: int, needed: int)
signal hp_changed(current: int, maximum: int)

var level: int = 1
var experience: int = 0
var experience_to_next: int = 100
var current_hp: int = 100

var stat_points_available: int = 0
var skill_points_available: int = 0

# Base stats (from level)
var base_hp: int = 100
var base_atk: int = 10
var base_def: int = 5
var base_spd: int = 5
var base_crit_rate: float = 0.05
var base_crit_dmg: float = 1.5

# Allocated stat points
var allocated_hp: int = 0
var allocated_atk: int = 0
var allocated_def: int = 0
var allocated_spd: int = 0
var allocated_crit_rate: int = 0
var allocated_crit_dmg: int = 0

# Equipment bonuses (set by EquipmentManager)
var equip_bonus_hp: int = 0
var equip_bonus_atk: int = 0
var equip_bonus_def: int = 0
var equip_bonus_spd: int = 0
var equip_bonus_crit_rate: float = 0.0
var equip_bonus_crit_dmg: float = 0.0

# Passive skill bonuses
var skill_bonus_hp: int = 0
var skill_bonus_atk: int = 0
var skill_bonus_def: int = 0
var skill_bonus_spd: int = 0
var skill_bonus_crit_rate: float = 0.0
var skill_bonus_crit_dmg: float = 0.0

# Building bonuses
var building_bonus_hp: int = 0
var building_bonus_atk: int = 0
var building_bonus_def: int = 0
var building_bonus_spd: int = 0
var building_bonus_crit_rate: float = 0.0
var building_bonus_crit_dmg: float = 0.0


func get_total_hp() -> int:
	return base_hp + allocated_hp * Constants.HP_PER_POINT + equip_bonus_hp + skill_bonus_hp + building_bonus_hp


func get_total_atk() -> int:
	return base_atk + allocated_atk * Constants.ATK_PER_POINT + equip_bonus_atk + skill_bonus_atk + building_bonus_atk


func get_total_def() -> int:
	return base_def + allocated_def * Constants.DEF_PER_POINT + equip_bonus_def + skill_bonus_def + building_bonus_def


func get_total_spd() -> int:
	return base_spd + allocated_spd * Constants.SPD_PER_POINT + equip_bonus_spd + skill_bonus_spd + building_bonus_spd


func get_total_crit_rate() -> float:
	return base_crit_rate + allocated_crit_rate * Constants.CRIT_RATE_PER_POINT + equip_bonus_crit_rate + skill_bonus_crit_rate + building_bonus_crit_rate


func get_total_crit_dmg() -> float:
	return base_crit_dmg + allocated_crit_dmg * Constants.CRIT_DMG_PER_POINT + equip_bonus_crit_dmg + skill_bonus_crit_dmg + building_bonus_crit_dmg


func add_experience(amount: int) -> void:
	experience += amount
	while experience >= experience_to_next:
		experience -= experience_to_next
		_level_up()
	experience_gained.emit(amount, experience, experience_to_next)


func _level_up() -> void:
	level += 1
	stat_points_available += Constants.STAT_PER_LEVEL
	skill_points_available += Constants.SKILL_POINT_PER_LEVEL
	experience_to_next = FormatUtils.xp_to_next_level(level)

	# Increase base stats slightly each level
	base_hp += 5
	base_atk += 1
	base_def += 1

	# Full heal on level up
	current_hp = get_total_hp()

	level_up.emit(level)
	stats_changed.emit()


func take_damage(damage: int) -> void:
	current_hp = maxi(0, current_hp - damage)
	hp_changed.emit(current_hp, get_total_hp())


func heal(amount: int) -> void:
	current_hp = mini(get_total_hp(), current_hp + amount)
	hp_changed.emit(current_hp, get_total_hp())


func full_heal() -> void:
	current_hp = get_total_hp()
	hp_changed.emit(current_hp, get_total_hp())


func allocate_stat(stat: int) -> void:
	if stat_points_available <= 0:
		return
	stat_points_available -= 1
	match stat:
		Constants.Stat.HP: allocated_hp += 1
		Constants.Stat.ATK: allocated_atk += 1
		Constants.Stat.DEF: allocated_def += 1
		Constants.Stat.SPD: allocated_spd += 1
		Constants.Stat.CRIT_RATE: allocated_crit_rate += 1
		Constants.Stat.CRIT_DMG: allocated_crit_dmg += 1
	if stat == Constants.Stat.HP:
		current_hp = mini(get_total_hp(), current_hp + Constants.HP_PER_POINT)
	stats_changed.emit()


func notify_stats_changed() -> void:
	stats_changed.emit()


func serialize() -> Dictionary:
	return {
		"level": level,
		"experience": experience,
		"experience_to_next": experience_to_next,
		"current_hp": current_hp,
		"stat_points_available": stat_points_available,
		"skill_points_available": skill_points_available,
		"base_hp": base_hp,
		"base_atk": base_atk,
		"base_def": base_def,
		"base_spd": base_spd,
		"allocated_hp": allocated_hp,
		"allocated_atk": allocated_atk,
		"allocated_def": allocated_def,
		"allocated_spd": allocated_spd,
		"allocated_crit_rate": allocated_crit_rate,
		"allocated_crit_dmg": allocated_crit_dmg,
	}


func deserialize(data: Dictionary) -> void:
	level = data.get("level", 1)
	experience = data.get("experience", 0)
	experience_to_next = data.get("experience_to_next", 100)
	current_hp = data.get("current_hp", Constants.BASE_PLAYER_HP)
	stat_points_available = data.get("stat_points_available", 0)
	skill_points_available = data.get("skill_points_available", 0)
	base_hp = data.get("base_hp", Constants.BASE_PLAYER_HP)
	base_atk = data.get("base_atk", Constants.BASE_PLAYER_ATK)
	base_def = data.get("base_def", Constants.BASE_PLAYER_DEF)
	base_spd = data.get("base_spd", Constants.BASE_PLAYER_SPD)
	allocated_hp = data.get("allocated_hp", 0)
	allocated_atk = data.get("allocated_atk", 0)
	allocated_def = data.get("allocated_def", 0)
	allocated_spd = data.get("allocated_spd", 0)
	allocated_crit_rate = data.get("allocated_crit_rate", 0)
	allocated_crit_dmg = data.get("allocated_crit_dmg", 0)
	stats_changed.emit()
