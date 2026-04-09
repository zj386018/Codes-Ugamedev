extends Node

signal stage_changed(new_stage: int)
signal stage_unlocked(stage_number: int)

var current_stage: int = 1
var highest_stage: int = 1
var monsters_killed_this_stage: int = 0
var boss_stages_cleared: Array[int] = []

# Monster definitions
var _monster_defs: Dictionary = {}  # id -> MonsterResource
var _boss_defs: Dictionary = {}


func _ready() -> void:
	_generate_monsters()


func _generate_monsters() -> void:
	# Normal monsters - cartoon colored blobs
	_add_monster("slime", "史莱姆", Color(0.3, 0.9, 0.3), 0.8, 50, 8, 3, 4, 5, 15, 20, false)
	_add_monster("goblin", "哥布林", Color(0.6, 0.8, 0.2), 0.9, 65, 12, 4, 5, 8, 20, 28, false)
	_add_monster("skeleton", "骷髅兵", Color(0.85, 0.85, 0.8), 1.0, 80, 15, 6, 5, 10, 25, 35, false)
	_add_monster("wolf", "灰狼", Color(0.5, 0.5, 0.5), 1.0, 70, 18, 4, 8, 8, 22, 32, false)
	_add_monster("mushroom", "毒蘑菇", Color(0.8, 0.3, 0.6), 0.7, 90, 10, 8, 3, 12, 28, 38, false)
	_add_monster("bat", "蝙蝠", Color(0.4, 0.2, 0.5), 0.6, 45, 20, 2, 10, 6, 18, 25, false)
	_add_monster("spider", "蜘蛛", Color(0.3, 0.2, 0.1), 0.9, 75, 14, 7, 6, 9, 24, 34, false)
	_add_monster("orc", "兽人", Color(0.5, 0.7, 0.3), 1.2, 120, 22, 10, 5, 15, 35, 50, false)
	_add_monster("ghost", "幽灵", Color(0.7, 0.7, 1.0), 0.9, 60, 16, 3, 12, 10, 26, 36, false)
	_add_monster("treant", "树人", Color(0.2, 0.6, 0.2), 1.4, 150, 12, 15, 3, 18, 40, 55, false)

	# Bosses
	_add_monster("slime_king", "史莱姆王", Color(0.2, 0.7, 0.2), 1.8, 300, 25, 15, 6, 50, 100, 120, true)
	_add_monster("goblin_chief", "哥布林酋长", Color(0.5, 0.6, 0.1), 1.6, 400, 35, 20, 8, 80, 150, 200, true)
	_add_monster("bone_dragon", "骨龙", Color(0.9, 0.9, 0.7), 2.0, 600, 50, 30, 10, 120, 250, 350, true)
	_add_monster("wolf_king", "狼王", Color(0.4, 0.4, 0.5), 1.7, 500, 45, 25, 12, 100, 200, 280, true)
	_add_monster("dark_mage", "暗黑法师", Color(0.3, 0.1, 0.4), 1.5, 450, 60, 15, 15, 150, 300, 400, true)
	_add_monster("demon_lord", "魔王", Color(0.8, 0.1, 0.1), 2.2, 1000, 80, 40, 15, 200, 500, 700, true)


func _add_monster(id: String, display_name: String, color: Color, size: float, hp: int, atk: int, defense: int, spd: int, gold_min: int, gold_max: int, xp: int, is_boss: bool) -> void:
	var monster := MonsterResource.new()
	monster.id = StringName(id)
	monster.name = id
	monster.display_name = display_name
	monster.color = color
	monster.size = size
	monster.base_hp = hp
	monster.base_atk = atk
	monster.base_def = defense
	monster.base_spd = spd
	monster.gold_drop_min = gold_min
	monster.gold_drop_max = gold_max
	monster.xp_reward = xp
	monster.is_boss = is_boss
	if is_boss:
		_boss_defs[StringName(id)] = monster
	else:
		_monster_defs[StringName(id)] = monster


func is_boss_stage(stage: int) -> bool:
	return stage > 0 and stage % 10 == 0


func get_monster_count(stage: int) -> int:
	if is_boss_stage(stage):
		return 1  # Just the boss
	return 3 + (stage / 20)  # More monsters in later stages


func get_monster_for_stage(stage: int) -> MonsterResource:
	var all_normal = _monster_defs.values()
	var index = (stage - 1) % all_normal.size()
	return all_normal[index]


func get_boss_for_stage(stage: int) -> MonsterResource:
	var all_bosses = _boss_defs.values()
	var boss_index = ((stage / 10) - 1) % all_bosses.size()
	return all_bosses[boss_index]


func advance_to_next_stage() -> void:
	current_stage += 1
	if current_stage > highest_stage:
		highest_stage = current_stage
		stage_unlocked.emit(current_stage)
	monsters_killed_this_stage = 0
	stage_changed.emit(current_stage)


func on_monster_killed() -> void:
	monsters_killed_this_stage += 1


func should_advance_stage() -> bool:
	var needed = get_monster_count(current_stage)
	return monsters_killed_this_stage >= needed


func on_boss_defeated(stage: int) -> void:
	if not boss_stages_cleared.has(stage):
		boss_stages_cleared.append(stage)


func reset_to_stage(stage: int) -> void:
	current_stage = stage
	monsters_killed_this_stage = 0
	stage_changed.emit(current_stage)


func serialize() -> Dictionary:
	return {
		"current_stage": current_stage,
		"highest_stage": highest_stage,
		"boss_stages_cleared": boss_stages_cleared,
	}


func deserialize(data: Dictionary) -> void:
	current_stage = data.get("current_stage", 1)
	highest_stage = data.get("highest_stage", 1)
	boss_stages_cleared.clear()
	for s in data.get("boss_stages_cleared", []):
		boss_stages_cleared.append(int(s))
	monsters_killed_this_stage = 0
	stage_changed.emit(current_stage)
