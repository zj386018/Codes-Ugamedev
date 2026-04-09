extends Node

signal item_equipped(slot: int, item: EquipmentResource)
signal item_unequipped(slot: int)
signal item_sold(item: EquipmentResource, gold_gained: int)
signal loot_dropped(item: EquipmentResource)
signal inventory_changed

# Equipped items: slot -> EquipmentResource
var equipped: Dictionary = {}
# Inventory: Array of EquipmentResource
var inventory: Array[EquipmentResource] = []

# All equipment definitions, loaded at startup
var _all_equipment: Array[EquipmentResource] = []


func _ready() -> void:
	# Initialize equipped slots
	for slot in Constants.EquipSlot.values():
		equipped[slot] = null
	_load_equipment_database()


func _load_equipment_database() -> void:
	# Generate equipment programmatically for the initial version
	var weapon_names = ["木剑", "铁剑", "精钢剑", "秘银剑", "传说之剑"]
	var armor_names = ["布甲", "皮甲", "锁子甲", "板甲", "龙鳞甲"]
	var helmet_names = ["布帽", "皮盔", "铁盔", "精钢盔", "王冠"]
	var boot_names = ["草鞋", "皮靴", "铁靴", "疾风靴", "飞行靴"]
	var accessory_names = ["铜戒指", "银戒指", "金戒指", "宝石戒指", "龙之戒"]

	var rarities = Constants.Rarity.values()
	var slots_data = [
		[Constants.EquipSlot.WEAPON, weapon_names, Color(0.8, 0.4, 0.2)],
		[Constants.EquipSlot.ARMOR, armor_names, Color(0.4, 0.4, 0.7)],
		[Constants.EquipSlot.HELMET, helmet_names, Color(0.6, 0.5, 0.3)],
		[Constants.EquipSlot.BOOTS, boot_names, Color(0.5, 0.3, 0.2)],
		[Constants.EquipSlot.ACCESSORY, accessory_names, Color(0.9, 0.8, 0.3)],
	]

	for slot_data in slots_data:
		var slot_type: int = slot_data[0]
		var names: Array = slot_data[1]
		var base_color: Color = slot_data[2]
		for rarity_idx in rarities.size():
			var rarity: int = rarities[rarity_idx]
			var rarity_mult: float = [1.0, 1.5, 2.5, 4.0, 7.0][rarity_idx]
			var item := EquipmentResource.new()
			item.id = StringName("%s_%d" % [Constants.SLOT_NAMES[slot_type], rarity_idx])
			item.name = names[rarity_idx]
			item.description = "%s品质的%s" % [Constants.RARITY_NAMES[rarity], Constants.SLOT_NAMES[slot_type]]
			item.rarity = rarity
			item.slot = slot_type
			item.sell_value = int(10 * rarity_mult)
			item.level_requirement = rarity_idx * 5 + 1
			# Stats scale with rarity
			if slot_type == Constants.EquipSlot.WEAPON:
				item.bonus_atk = int(5 * rarity_mult)
				item.bonus_crit_rate = 0.02 * rarity_idx
				item.bonus_crit_dmg = 0.1 * rarity_idx
			elif slot_type == Constants.EquipSlot.ARMOR:
				item.bonus_hp = int(20 * rarity_mult)
				item.bonus_def = int(3 * rarity_mult)
			elif slot_type == Constants.EquipSlot.HELMET:
				item.bonus_hp = int(10 * rarity_mult)
				item.bonus_def = int(2 * rarity_mult)
				item.bonus_spd = rarity_idx
			elif slot_type == Constants.EquipSlot.BOOTS:
				item.bonus_spd = int(2 + rarity_idx * 2)
				item.bonus_hp = int(5 * rarity_mult)
			elif slot_type == Constants.EquipSlot.ACCESSORY:
				item.bonus_crit_rate = 0.03 * rarity_idx + 0.01
				item.bonus_crit_dmg = 0.15 * rarity_idx
				item.bonus_atk = int(2 * rarity_mult)
			_all_equipment.append(item)


func equip_item(item: EquipmentResource) -> void:
	if item == null:
		return
	# Unequip current item in that slot
	var current = equipped.get(item.slot)
	if current != null:
		inventory.append(current)
	# Remove from inventory
	inventory.erase(item)
	equipped[item.slot] = item
	_recalculate_equipment_bonuses()
	item_equipped.emit(item.slot, item)
	inventory_changed.emit()


func unequip_item(slot: int) -> void:
	var item = equipped.get(slot)
	if item == null:
		return
	inventory.append(item)
	equipped[slot] = null
	_recalculate_equipment_bonuses()
	item_unequipped.emit(slot)
	inventory_changed.emit()


func sell_item(item: EquipmentResource) -> void:
	var gold_gained = item.sell_value
	inventory.erase(item)
	EconomyManager.add_gold(gold_gained)
	item_sold.emit(item, gold_gained)
	inventory_changed.emit()


func add_item_to_inventory(item: EquipmentResource) -> void:
	inventory.append(item)
	inventory_changed.emit()


func get_random_drop(stage: int) -> EquipmentResource:
	# Higher stages = better chance of rare items
	var roll = randf()
	var rarity: int
	if stage >= 50 and roll < 0.02:
		rarity = Constants.Rarity.LEGENDARY
	elif stage >= 30 and roll < 0.08:
		rarity = Constants.Rarity.EPIC
	elif stage >= 15 and roll < 0.20:
		rarity = Constants.Rarity.RARE
	elif roll < 0.40:
		rarity = Constants.Rarity.UNCOMMON
	else:
		rarity = Constants.Rarity.COMMON

	# Filter by rarity
	var candidates = _all_equipment.filter(func(e): return e.rarity == rarity)
	if candidates.is_empty():
		candidates = _all_equipment.filter(func(e): return e.rarity == Constants.Rarity.COMMON)

	# Pick random slot type
	var chosen = candidates[randi() % candidates.size()]
	var drop := chosen.duplicate()
	# Add some randomness to stats
	drop.bonus_atk = maxi(1, drop.bonus_atk + randi_range(-1, 2))
	drop.bonus_hp = maxi(1, drop.bonus_hp + randi_range(-3, 5))
	return drop


func roll_loot(stage: int) -> void:
	# Base drop chance
	var drop_chance = 0.08 + stage * 0.001
	if randf() < drop_chance:
		var item = get_random_drop(stage)
		add_item_to_inventory(item)
		loot_dropped.emit(item)


func _recalculate_equipment_bonuses() -> void:
	PlayerData.equip_bonus_hp = 0
	PlayerData.equip_bonus_atk = 0
	PlayerData.equip_bonus_def = 0
	PlayerData.equip_bonus_spd = 0
	PlayerData.equip_bonus_crit_rate = 0.0
	PlayerData.equip_bonus_crit_dmg = 0.0

	for slot in equipped:
		var item: EquipmentResource = equipped[slot]
		if item == null:
			continue
		PlayerData.equip_bonus_hp += item.bonus_hp
		PlayerData.equip_bonus_atk += item.bonus_atk
		PlayerData.equip_bonus_def += item.bonus_def
		PlayerData.equip_bonus_spd += item.bonus_spd
		PlayerData.equip_bonus_crit_rate += item.bonus_crit_rate
		PlayerData.equip_bonus_crit_dmg += item.bonus_crit_dmg

	PlayerData.notify_stats_changed()


func serialize() -> Dictionary:
	var equipped_data = {}
	for slot in equipped:
		var item: EquipmentResource = equipped[slot]
		if item != null:
			equipped_data[str(slot)] = {
				"name": item.name,
				"rarity": item.rarity,
				"slot": item.slot,
				"bonus_hp": item.bonus_hp,
				"bonus_atk": item.bonus_atk,
				"bonus_def": item.bonus_def,
				"bonus_spd": item.bonus_spd,
				"bonus_crit_rate": item.bonus_crit_rate,
				"bonus_crit_dmg": item.bonus_crit_dmg,
				"sell_value": item.sell_value,
				"level_requirement": item.level_requirement,
			}
		else:
			equipped_data[str(slot)] = null

	var inv_data = []
	for item in inventory:
		inv_data.append({
			"name": item.name,
			"rarity": item.rarity,
			"slot": item.slot,
			"bonus_hp": item.bonus_hp,
			"bonus_atk": item.bonus_atk,
			"bonus_def": item.bonus_def,
			"bonus_spd": item.bonus_spd,
			"bonus_crit_rate": item.bonus_crit_rate,
			"bonus_crit_dmg": item.bonus_crit_dmg,
			"sell_value": item.sell_value,
			"level_requirement": item.level_requirement,
		})

	return {
		"equipped": equipped_data,
		"inventory": inv_data,
	}


func deserialize(data: Dictionary) -> void:
	# Clear
	for slot in Constants.EquipSlot.values():
		equipped[slot] = null
	inventory.clear()

	# Load equipped
	var equipped_data = data.get("equipped", {})
	for slot_key in equipped_data:
		var slot_val = int(slot_key)
		var item_data = equipped_data[slot_key]
		if item_data != null:
			var item := EquipmentResource.new()
			item.name = item_data.get("name", "")
			item.rarity = item_data.get("rarity", 0)
			item.slot = item_data.get("slot", 0)
			item.bonus_hp = item_data.get("bonus_hp", 0)
			item.bonus_atk = item_data.get("bonus_atk", 0)
			item.bonus_def = item_data.get("bonus_def", 0)
			item.bonus_spd = item_data.get("bonus_spd", 0)
			item.bonus_crit_rate = item_data.get("bonus_crit_rate", 0.0)
			item.bonus_crit_dmg = item_data.get("bonus_crit_dmg", 0.0)
			item.sell_value = item_data.get("sell_value", 10)
			item.level_requirement = item_data.get("level_requirement", 1)
			equipped[slot_val] = item

	# Load inventory
	var inv_data = data.get("inventory", [])
	for item_data in inv_data:
		var item := EquipmentResource.new()
		item.name = item_data.get("name", "")
		item.rarity = item_data.get("rarity", 0)
		item.slot = item_data.get("slot", 0)
		item.bonus_hp = item_data.get("bonus_hp", 0)
		item.bonus_atk = item_data.get("bonus_atk", 0)
		item.bonus_def = item_data.get("bonus_def", 0)
		item.bonus_spd = item_data.get("bonus_spd", 0)
		item.bonus_crit_rate = item_data.get("bonus_crit_rate", 0.0)
		item.bonus_crit_dmg = item_data.get("bonus_crit_dmg", 0.0)
		item.sell_value = item_data.get("sell_value", 10)
		item.level_requirement = item_data.get("level_requirement", 1)
		inventory.append(item)

	_recalculate_equipment_bonuses()
	inventory_changed.emit()
