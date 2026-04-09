class_name BuildingResource
extends Resource

@export var id: StringName = &""
@export var name: String = ""
@export var description: String = ""
@export var icon: Texture2D
@export var building_type: int = Constants.BuildingType.GOLD_MINE
@export var base_cost: int = 100
@export var cost_growth_rate: float = 1.5
@export var max_level: int = 50
@export var base_output: float = 1.0
@export var output_growth_rate: float = 1.2
@export var affected_stat: int = Constants.Stat.NONE
@export var color: Color = Color.YELLOW


func get_upgrade_cost(current_level: int) -> int:
	return int(base_cost * pow(cost_growth_rate, current_level))


func get_output(current_level: int) -> float:
	return base_output * pow(output_growth_rate, current_level - 1)
