extends Node

signal item_purchased(item_id: StringName)
signal shop_refreshed

var _shop_items: Array[Dictionary] = []
var _refresh_timer: float = 0.0
var _refresh_interval: float = 3600.0  # 1 hour
var _purchased_today: Array[String] = []

func _ready() -> void:
	_refresh_shop()


func _process(delta: float) -> void:
	_refresh_timer -= delta
	if _refresh_timer <= 0:
		_refresh_shop()


func get_refresh_time_remaining() -> float:
	return maxf(0.0, _refresh_timer)


func get_shop_items() -> Array[Dictionary]:
	return _shop_items


func purchase_item(index: int) -> bool:
	if index < 0 or index >= _shop_items.size():
		return false
	var item = _shop_items[index]
	var currency_type: String = item.get("currency", "gold")
	var cost: int = item.get("cost", 0)

	if currency_type == "gold":
		if not EconomyManager.spend_gold(cost):
			return false
	elif currency_type == "gems":
		if not EconomyManager.spend_gems(cost):
			return false

	# Apply purchase
	var item_type: String = item.get("type", "")
	match item_type:
		"equipment_pack":
			var rarity = item.get("rarity", Constants.Rarity.COMMON)
			var equip = _generate_random_equipment(rarity)
			EquipmentManager.add_item_to_inventory(equip)
		"xp_boost":
			# For now, just give instant XP
			PlayerData.add_experience(item.get("value", 100))
		"gold_pack":
			EconomyManager.add_gold(item.get("value", 500))

	_purchased_today.append(item.get("id", ""))
	item_purchased.emit(StringName(item.get("id", "")))
	return true


func _refresh_shop() -> void:
	_shop_items.clear()
	_purchased_today.clear()
	_refresh_timer = _refresh_interval

	# Equipment packs
	_shop_items.append({
		"id": "eq_pack_common",
		"name": "普通装备包",
		"description": "随机获得一件普通品质装备",
		"type": "equipment_pack",
		"rarity": Constants.Rarity.COMMON,
		"cost": 100,
		"currency": "gold",
	})

	_shop_items.append({
		"id": "eq_pack_rare",
		"name": "稀有装备包",
		"description": "随机获得一件稀有品质装备",
		"type": "equipment_pack",
		"rarity": Constants.Rarity.RARE,
		"cost": 500,
		"currency": "gold",
	})

	_shop_items.append({
		"id": "eq_pack_epic",
		"name": "史诗装备包",
		"description": "随机获得一件史诗品质装备",
		"type": "equipment_pack",
		"rarity": Constants.Rarity.EPIC,
		"cost": 2000,
		"currency": "gold",
	})

	# XP boost
	_shop_items.append({
		"id": "xp_boost_small",
		"name": "经验丹(小)",
		"description": "立即获得500经验",
		"type": "xp_boost",
		"value": 500,
		"cost": 200,
		"currency": "gold",
	})

	_shop_items.append({
		"id": "xp_boost_large",
		"name": "经验丹(大)",
		"description": "立即获得3000经验",
		"type": "xp_boost",
		"value": 3000,
		"cost": 1000,
		"currency": "gold",
	})

	# Gold pack
	_shop_items.append({
		"id": "gold_pack",
		"name": "金币袋",
		"description": "立即获得2000金币",
		"type": "gold_pack",
		"value": 2000,
		"cost": 20,
		"currency": "gems",
	})

	shop_refreshed.emit()


func _generate_random_equipment(min_rarity: int) -> EquipmentResource:
	var all = EquipmentManager._all_equipment.filter(func(e): return e.rarity >= min_rarity)
	if all.is_empty():
		all = EquipmentManager._all_equipment
	var chosen = all[randi() % all.size()]
	return chosen.duplicate()


func serialize() -> Dictionary:
	return {
		"refresh_timer": _refresh_timer,
		"purchased_today": _purchased_today,
	}


func deserialize(data: Dictionary) -> void:
	_refresh_timer = data.get("refresh_timer", _refresh_interval)
	_purchased_today.clear()
	for p in data.get("purchased_today", []):
		_purchased_today.append(p)
