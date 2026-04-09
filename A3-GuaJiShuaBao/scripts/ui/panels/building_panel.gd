extends Control

@onready var building_grid: GridContainer = $VBox/ScrollContainer/BuildingGrid


func _ready() -> void:
	BuildingManager.building_upgraded.connect(func(_a, _b): _refresh())
	_refresh()


func _refresh() -> void:
	for child in building_grid.get_children():
		child.queue_free()

	var building_ids = BuildingManager.get_all_building_ids()

	for building_id in building_ids:
		var building: BuildingResource = BuildingManager.get_building_def(building_id)
		var level: int = BuildingManager.get_building_level(building_id)

		var card = Panel.new()
		var vbox = VBoxContainer.new()
		vbox.add_theme_constant_override("separation", 4)

		# Name and level
		var title = Label.new()
		title.text = "%s Lv.%d/%d" % [building.name, level, building.max_level]
		title.add_theme_color_override("font_color", building.color)
		vbox.add_child(title)

		# Description
		var desc = Label.new()
		desc.text = building.description
		desc.add_theme_font_size_override("font_size", 12)
		desc.add_theme_color_override("font_color", Color.LIGHT_GRAY)
		vbox.add_child(desc)

		# Current output
		var output_label = Label.new()
		if level > 0:
			match building.building_type:
				Constants.BuildingType.GOLD_MINE:
					output_label.text = "产出: %.1f 金币/秒" % building.get_output(level)
				Constants.BuildingType.XP_SHRINE:
					output_label.text = "产出: %.1f 经验/秒" % building.get_output(level)
				Constants.BuildingType.BLACKSMITH:
					output_label.text = "装备掉落品质提升"
				Constants.BuildingType.TRAINING_GROUND:
					output_label.text = "攻击力: +%d" % int(building.get_output(level))
		else:
			output_label.text = "未建造"
		vbox.add_child(output_label)

		# Upgrade button
		var btn = Button.new()
		var cost = BuildingManager.get_upgrade_cost(building_id)
		if level >= building.max_level:
			btn.text = "已满级"
			btn.disabled = true
		else:
			if level == 0:
				btn.text = "建造 (%d金)" % cost
			else:
				btn.text = "升级 (%d金)" % cost
			if not EconomyManager.can_afford_gold(cost):
				btn.disabled = true
		var bid = building_id
		btn.pressed.connect(func(): BuildingManager.upgrade_building(bid))
		vbox.add_child(btn)

		card.add_child(vbox)
		card.custom_minimum_size = Vector2(320, 140)
		building_grid.add_child(card)
