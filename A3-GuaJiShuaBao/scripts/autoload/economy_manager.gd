extends Node

signal gold_changed(new_amount: int, delta: int)
signal gems_changed(new_amount: int, delta: int)
signal cannot_afford(item_name: String)

var gold: int = 0
var gems: int = 0
var total_gold_earned: int = 0


func add_gold(amount: int) -> void:
	gold += amount
	total_gold_earned += amount
	gold_changed.emit(gold, amount)


func spend_gold(amount: int) -> bool:
	if gold < amount:
		return false
	gold -= amount
	gold_changed.emit(gold, -amount)
	return true


func add_gems(amount: int) -> void:
	gems += amount
	gems_changed.emit(gems, amount)


func spend_gems(amount: int) -> bool:
	if gems < amount:
		return false
	gems -= amount
	gems_changed.emit(gems, -amount)
	return true


func can_afford_gold(amount: int) -> bool:
	return gold >= amount


func can_afford_gems(amount: int) -> bool:
	return gems >= amount


func serialize() -> Dictionary:
	return {
		"gold": gold,
		"gems": gems,
		"total_gold_earned": total_gold_earned,
	}


func deserialize(data: Dictionary) -> void:
	gold = data.get("gold", 0)
	gems = data.get("gems", 0)
	total_gold_earned = data.get("total_gold_earned", 0)
	gold_changed.emit(gold, 0)
	gems_changed.emit(gems, 0)
