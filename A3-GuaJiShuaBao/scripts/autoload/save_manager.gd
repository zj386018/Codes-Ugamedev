extends Node

signal game_saved(slot: int)
signal game_loaded(slot: int)
signal save_failed(error: String)

var _dirty: bool = false
var _auto_save_timer: float = 0.0
var _current_slot: int = 0

func _ready() -> void:
	# Connect to signals that mark save as dirty
	PlayerData.stats_changed.connect(func(): _dirty = true)
	EconomyManager.gold_changed.connect(func(_a, _b): _dirty = true)
	EquipmentManager.inventory_changed.connect(func(): _dirty = true)
	BuildingManager.building_upgraded.connect(func(_a, _b): _dirty = true)
	StageManager.stage_changed.connect(func(_a): _dirty = true)


func _process(delta: float) -> void:
	_auto_save_timer += delta
	if _auto_save_timer >= Constants.AUTO_SAVE_INTERVAL and _dirty:
		_auto_save_timer = 0.0
		save_game()


func save_game(slot: int = -1) -> void:
	if slot >= 0:
		_current_slot = slot
	var data = _collect_save_data()
	var json_string = JSON.stringify(data, "\t")
	var path = "user://save_slot_%d.json" % _current_slot
	var file = FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		save_failed.emit("Cannot open file for writing")
		return
	file.store_string(json_string)
	file.close()
	_dirty = false
	game_saved.emit(_current_slot)


func load_game(slot: int = 0) -> bool:
	var path = "user://save_slot_%d.json" % slot
	if not FileAccess.file_exists(path):
		return false
	var file = FileAccess.open(path, FileAccess.READ)
	if file == null:
		return false
	var json_string = file.get_as_text()
	file.close()
	var json = JSON.new()
	var error = json.parse(json_string)
	if error != OK:
		save_failed.emit("Parse error: " + json.get_error_message())
		return false
	var data = json.data
	if not data is Dictionary:
		return false
	_current_slot = slot
	_distribute_save_data(data)
	game_loaded.emit(slot)
	return true


func has_save(slot: int = 0) -> bool:
	return FileAccess.file_exists("user://save_slot_%d.json" % slot)


func delete_save(slot: int = 0) -> void:
	var path = "user://save_slot_%d.json" % slot
	if FileAccess.file_exists(path):
		DirAccess.remove_absolute(path)


func calculate_offline_rewards() -> Dictionary:
	var path = "user://save_slot_%d.json" % _current_slot
	if not FileAccess.file_exists(path):
		return {"gold": 0, "xp": 0}
	var file = FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {"gold": 0, "xp": 0}
	var json_string = file.get_as_text()
	file.close()
	var json = JSON.new()
	json.parse(json_string)
	var data = json.data

	var saved_timestamp = data.get("timestamp", 0.0)
	var offline_seconds = TimeManager.calculate_offline_time(saved_timestamp)
	var gold_per_sec = BuildingManager.get_gold_per_second()
	var xp_per_sec = BuildingManager.get_xp_per_second()
	var efficiency = Constants.OFFLINE_EFFICIENCY

	return {
		"gold": int(gold_per_sec * offline_seconds * efficiency),
		"xp": int(xp_per_sec * offline_seconds * efficiency),
		"seconds": offline_seconds,
	}


func _collect_save_data() -> Dictionary:
	return {
		"version": 1,
		"timestamp": TimeManager.get_current_timestamp(),
		"player": PlayerData.serialize(),
		"economy": EconomyManager.serialize(),
		"equipment": EquipmentManager.serialize(),
		"skills": SkillManager.serialize(),
		"buildings": BuildingManager.serialize(),
		"stage": StageManager.serialize(),
		"battle": BattleManager.serialize(),
		"shop": ShopManager.serialize(),
	}


func _distribute_save_data(data: Dictionary) -> void:
	PlayerData.deserialize(data.get("player", {}))
	EconomyManager.deserialize(data.get("economy", {}))
	EquipmentManager.deserialize(data.get("equipment", {}))
	SkillManager.deserialize(data.get("skills", {}))
	BuildingManager.deserialize(data.get("buildings", {}))
	StageManager.deserialize(data.get("stage", {}))
	BattleManager.deserialize(data.get("battle", {}))
	ShopManager.deserialize(data.get("shop", {}))
