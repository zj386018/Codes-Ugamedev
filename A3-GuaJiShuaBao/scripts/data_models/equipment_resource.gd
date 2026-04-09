class_name EquipmentResource
extends Resource

@export var id: StringName = &""
@export var name: String = ""
@export var description: String = ""
@export var icon: Texture2D
@export var rarity: int = Constants.Rarity.COMMON
@export var sell_value: int = 10
@export var slot: int = Constants.EquipSlot.WEAPON
@export var bonus_hp: int = 0
@export var bonus_atk: int = 0
@export var bonus_def: int = 0
@export var bonus_spd: int = 0
@export var bonus_crit_rate: float = 0.0
@export var bonus_crit_dmg: float = 0.0
@export var level_requirement: int = 1


func get_total_power() -> int:
	return bonus_hp / 5 + bonus_atk * 2 + bonus_def * 2 + bonus_spd + int(bonus_crit_rate * 100) + int(bonus_crit_dmg * 10)
