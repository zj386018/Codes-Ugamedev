extends Node

signal toast_requested(message: String)
signal loot_popup_requested(item_name: String, rarity: int)
signal level_up_requested(new_level: int)

var _toast_queue: Array[String] = []
var _is_showing_toast: bool = false


func show_toast(message: String) -> void:
	toast_requested.emit(message)


func show_loot_popup(item_name: String, rarity: int) -> void:
	loot_popup_requested.emit(item_name, rarity)


func show_level_up(new_level: int) -> void:
	level_up_requested.emit(new_level)


func serialize() -> Dictionary:
	return {}


func deserialize(_data: Dictionary) -> void:
	pass
