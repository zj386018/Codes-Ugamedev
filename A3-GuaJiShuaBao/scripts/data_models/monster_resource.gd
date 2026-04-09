class_name MonsterResource
extends Resource

@export var id: StringName = &""
@export var name: String = ""
@export var display_name: String = ""
@export var color: Color = Color.GREEN
@export var size: float = 1.0
@export var base_hp: int = 50
@export var base_atk: int = 8
@export var base_def: int = 3
@export var base_spd: int = 4
@export var gold_drop_min: int = 5
@export var gold_drop_max: int = 15
@export var xp_reward: int = 20
@export var is_boss: bool = false
@export var scale_per_stage: float = 1.12
@export var equipment_drop_chance: float = 0.1


func get_scaled_hp(stage: int) -> int:
	return int(base_hp * pow(scale_per_stage, stage - 1))


func get_scaled_atk(stage: int) -> int:
	return int(base_atk * pow(scale_per_stage, stage - 1))


func get_scaled_def(stage: int) -> int:
	return int(base_def * pow(scale_per_stage, stage - 1))


func get_scaled_spd(stage: int) -> int:
	return int(base_spd * pow(scale_per_stage, stage - 1))


func get_gold_drop() -> int:
	return randi_range(gold_drop_min, gold_drop_max)
