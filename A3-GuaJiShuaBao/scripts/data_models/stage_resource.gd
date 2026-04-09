class_name StageResource
extends Resource

@export var stage_number: int = 1
@export var chapter: int = 1
@export var monster_pool: Array[MonsterResource] = []
@export var boss_monster: MonsterResource
@export var is_boss_stage: bool = false
@export var monster_count: int = 5
@export var gold_bonus_mult: float = 1.0
@export var xp_bonus_mult: float = 1.0
@export var bg_color: Color = Color(0.15, 0.15, 0.2)
