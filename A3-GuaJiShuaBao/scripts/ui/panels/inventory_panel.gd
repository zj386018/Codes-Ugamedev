extends Control

@onready var grid: GridContainer = $VBox/ScrollContainer/Grid
@onready var sort_btn: Button = $VBox/SortBar/SortBtn
@onready var item_detail: Panel = $VBox/ItemDetail
@onready var detail_name: Label = $VBox/ItemDetail/VBox/NameLabel
@onready var detail_stats: Label = $VBox/ItemDetail/VBox/StatsLabel
@onready var equip_btn: Button = $VBox/ItemDetail/VBox/EquipBtn
@onready var sell_btn: Button = $VBox/ItemDetail/VBox/SellBtn

var _selected_index: int = -1


func _ready() -> void:
	EquipmentManager.inventory_changed.connect(_refresh_inventory)
	sort_btn.pressed.connect(_sort_inventory)
	equip_btn.pressed.connect(_equip_selected)
	sell_btn.pressed.connect(_sell_selected)
	item_detail.visible = false
	_refresh_inventory()


func _refresh_inventory() -> void:
	# Clear grid
	for child in grid.get_children():
		child.queue_free()

	# Create item buttons
	for i in EquipmentManager.inventory.size():
		var item: EquipmentResource = EquipmentManager.inventory[i]
		var btn = Button.new()
		btn.text = "%s [%s]" % [item.name, Constants.RARITY_NAMES[item.rarity]]
		btn.custom_minimum_size = Vector2(160, 40)
		var rarity_color = Constants.RARITY_COLORS[item.rarity]
		btn.add_theme_color_override("font_color", rarity_color)
		var index = i
		btn.pressed.connect(func(): _select_item(index))
		grid.add_child(btn)

	# Equipped items header
	var sep = HSeparator.new()
	grid.add_child(sep)
	var equipped_label = Label.new()
	equipped_label.text = "--- 已装备 ---"
	equipped_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	grid.add_child(equipped_label)

	for slot in Constants.EquipSlot.values():
		var item: EquipmentResource = EquipmentManager.equipped.get(slot)
		var btn = Button.new()
		if item:
			btn.text = "%s: %s [%s]" % [Constants.SLOT_NAMES[slot], item.name, Constants.RARITY_NAMES[item.rarity]]
			btn.add_theme_color_override("font_color", Constants.RARITY_COLORS[item.rarity])
		else:
			btn.text = "%s: (空)" % Constants.SLOT_NAMES[slot]
		btn.custom_minimum_size = Vector2(160, 40)
		btn.pressed.connect(func(): EquipmentManager.unequip_item(slot))
		grid.add_child(btn)

	item_detail.visible = false


func _select_item(index: int) -> void:
	if index < 0 or index >= EquipmentManager.inventory.size():
		return
	_selected_index = index
	var item: EquipmentResource = EquipmentManager.inventory[index]
	detail_name.text = "%s [%s]" % [item.name, Constants.RARITY_NAMES[item.rarity]]
	detail_name.add_theme_color_override("font_color", Constants.RARITY_COLORS[item.rarity])
	var stats_text = "攻击: +%d\n防御: +%d\n生命: +%d\n速度: +%d\n暴击率: +%.1f%%\n暴击伤害: +%.1fx" % [
		item.bonus_atk, item.bonus_def, item.bonus_hp, item.bonus_spd,
		item.bonus_crit_rate * 100, item.bonus_crit_dmg
	]
	detail_stats.text = stats_text
	equip_btn.text = "装备 (%s)" % Constants.SLOT_NAMES[item.slot]
	sell_btn.text = "出售 (%d金)" % item.sell_value
	item_detail.visible = true


func _equip_selected() -> void:
	if _selected_index < 0 or _selected_index >= EquipmentManager.inventory.size():
		return
	var item = EquipmentManager.inventory[_selected_index]
	EquipmentManager.equip_item(item)
	_selected_index = -1


func _sell_selected() -> void:
	if _selected_index < 0 or _selected_index >= EquipmentManager.inventory.size():
		return
	var item = EquipmentManager.inventory[_selected_index]
	EquipmentManager.sell_item(item)
	_selected_index = -1


func _sort_inventory() -> void:
	EquipmentManager.inventory.sort_custom(func(a, b): return a.rarity > b.rarity)
	_refresh_inventory()
