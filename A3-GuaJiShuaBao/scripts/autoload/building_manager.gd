extends Node

signal building_upgraded(building_id: StringName, new_level: int)
signal resources_produced(resource_type: String, amount: float)
signal production_tick(delta: float)

# building_id -> level
var building_levels: Dictionary = {}
# building definitions
var _building_defs: Dictionary = {}  # building_id -> BuildingResource
# Accumulated time for production
var _production_accumulator: float = 0.0

func _ready() -> void:
	_generate_buildings()


func _generate_buildings() -> void:
	_add_building("gold_mine", "金矿", "持续产出金币", Constants.BuildingType.GOLD_MINE, 50, 1.5, 50, 2.0, 1.15, Constants.Stat.NONE, Color(1.0, 0.85, 0.0))
	_add_building("xp_shrine", "经验神殿", "持续产出经验值", Constants.BuildingType.XP_SHRINE, 80, 1.6, 50, 1.5, 1.18, Constants.Stat.NONE, Color(0.3, 0.7, 1.0))
	_add_building("blacksmith", "铁匠铺", "提升装备掉落品质", Constants.BuildingType.BLACKSMITH, 150, 1.7, 30, 0.0, 1.0, Constants.Stat.NONE, Color(0.8, 0.4, 0.2))
	_add_building("training_ground", "训练场", "提升角色属性", Constants.BuildingType.TRAINING_GROUND, 120, 1.6, 50, 1.0, 1.15, Constants.Stat.ATK, Color(0.5, 0.8, 0.3))

	for building_id in _building_defs:
		building_levels[building_id] = 0


func _add_building(id: String, bname: String, desc: String, type: int, base_cost: int, cost_growth: float, max_lvl: int, base_out: float, out_growth: float, stat: int, color: Color) -> void:
	var building := BuildingResource.new()
	building.id = StringName(id)
	building.name = bname
	building.description = desc
	building.building_type = type
	building.base_cost = base_cost
	building.cost_growth_rate = cost_growth
	building.max_level = max_lvl
	building.base_output = base_out
	building.output_growth_rate = out_growth
	building.affected_stat = stat
	building.color = color
	_building_defs[StringName(id)] = building


func _process(delta: float) -> void:
	_production_accumulator += delta

	if _production_accumulator >= 1.0:
		var ticks = int(_production_accumulator)
		_production_accumulator -= ticks

		for building_id in building_levels:
			var level: int = building_levels[building_id]
			if level <= 0:
				continue
			var building: BuildingResource = _building_defs[building_id]
			var output = building.get_output(level) * ticks

			match building.building_type:
				Constants.BuildingType.GOLD_MINE:
					EconomyManager.add_gold(int(output))
					resources_produced.emit("gold", output)
				Constants.BuildingType.XP_SHRINE:
					PlayerData.add_experience(int(output))
					resources_produced.emit("xp", output)
				Constants.BuildingType.TRAINING_GROUND:
					pass  # Applied as static bonus

		production_tick.emit(delta)


func can_upgrade(building_id: StringName) -> bool:
	var level: int = building_levels.get(building_id, 0)
	var building: BuildingResource = _building_defs.get(building_id)
	if building == null:
		return false
	if level >= building.max_level:
		return false
	var cost = building.get_upgrade_cost(level)
	return EconomyManager.can_afford_gold(cost)


func upgrade_building(building_id: StringName) -> bool:
	if not can_upgrade(building_id):
		return false
	var building: BuildingResource = _building_defs[building_id]
	var level: int = building_levels[building_id]
	var cost = building.get_upgrade_cost(level)
	if not EconomyManager.spend_gold(cost):
		return false
	building_levels[building_id] = level + 1
	_apply_building_bonuses()
	building_upgraded.emit(building_id, level + 1)
	return true


func get_upgrade_cost(building_id: StringName) -> int:
	var level: int = building_levels.get(building_id, 0)
	var building: BuildingResource = _building_defs.get(building_id)
	if building == null:
		return 0
	return building.get_upgrade_cost(level)


func get_building_level(building_id: StringName) -> int:
	return building_levels.get(building_id, 0)


func get_building_def(building_id: StringName) -> BuildingResource:
	return _building_defs.get(building_id)


func get_all_building_ids() -> Array[StringName]:
	var ids: Array[StringName] = []
	for id in _building_defs:
		ids.append(id)
	return ids


func _apply_building_bonuses() -> void:
	PlayerData.building_bonus_hp = 0
	PlayerData.building_bonus_atk = 0
	PlayerData.building_bonus_def = 0
	PlayerData.building_bonus_spd = 0
	PlayerData.building_bonus_crit_rate = 0.0
	PlayerData.building_bonus_crit_dmg = 0.0

	for building_id in building_levels:
		var level: int = building_levels[building_id]
		if level <= 0:
			continue
		var building: BuildingResource = _building_defs[building_id]
		if building.building_type != Constants.BuildingType.TRAINING_GROUND:
			continue
		var output = building.get_output(level)
		PlayerData.building_bonus_atk += int(output)

	PlayerData.notify_stats_changed()


func get_gold_per_second() -> float:
	var total = 0.0
	for building_id in building_levels:
		var level: int = building_levels[building_id]
		if level <= 0:
			continue
		var building: BuildingResource = _building_defs[building_id]
		if building.building_type == Constants.BuildingType.GOLD_MINE:
			total += building.get_output(level)
	return total


func get_xp_per_second() -> float:
	var total = 0.0
	for building_id in building_levels:
		var level: int = building_levels[building_id]
		if level <= 0:
			continue
		var building: BuildingResource = _building_defs[building_id]
		if building.building_type == Constants.BuildingType.XP_SHRINE:
			total += building.get_output(level)
	return total


func serialize() -> Dictionary:
	return { "levels": building_levels.duplicate() }


func deserialize(data: Dictionary) -> void:
	building_levels.clear()
	var levels = data.get("levels", {})
	for id_key in levels:
		building_levels[StringName(id_key)] = levels[id_key]
	_apply_building_bonuses()
