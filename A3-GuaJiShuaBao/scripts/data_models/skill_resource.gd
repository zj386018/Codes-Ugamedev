class_name SkillResource
extends Resource

@export var id: StringName = &""
@export var name: String = ""
@export var description: String = ""
@export var icon: Texture2D
@export var skill_type: int = Constants.SkillType.ACTIVE
@export var max_level: int = 10
@export var prerequisites: Array[StringName] = []
@export var grid_position: Vector2 = Vector2.ZERO

# Active skill properties
@export var cooldown_seconds: float = 5.0
@export var damage_multiplier_base: float = 1.5
@export var damage_multiplier_per_level: float = 0.3

# Passive skill properties
@export var passive_stat: int = Constants.Stat.NONE
@export var passive_bonus_base: float = 0.05
@export var passive_bonus_per_level: float = 0.03


func get_damage_multiplier(skill_level: int) -> float:
	return damage_multiplier_base + damage_multiplier_per_level * (skill_level - 1)


func get_passive_bonus(skill_level: int) -> float:
	return passive_bonus_base + passive_bonus_per_level * (skill_level - 1)
