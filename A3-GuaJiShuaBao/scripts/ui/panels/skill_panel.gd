extends Control

@onready var points_label: Label = $VBox/PointsLabel
@onready var equipped_container: HBoxContainer = $VBox/EquippedContainer
@onready var skill_list: VBoxContainer = $VBox/ScrollContainer/SkillList


func _ready() -> void:
	PlayerData.stats_changed.connect(_refresh)
	SkillManager.skill_unlocked.connect(func(_s): _refresh())
	SkillManager.skill_upgraded.connect(func(_s, _l): _refresh())
	_refresh()


func _refresh() -> void:
	points_label.text = "技能点数: %d" % PlayerData.skill_points_available

	# Clear
	for child in equipped_container.get_children():
		child.queue_free()
	for child in skill_list.get_children():
		child.queue_free()

	# Equipped active skills
	var eq_label = Label.new()
	eq_label.text = "已装备主动技能:"
	equipped_container.add_child(eq_label)

	for i in Constants.MAX_EQUIPPED_SKILLS:
		var btn = Button.new()
		var skill_id: StringName = SkillManager.equipped_skills[i]
		if skill_id != &"":
			var def: SkillResource = SkillManager.get_skill_definition(skill_id)
			btn.text = "%s Lv%d" % [def.name, SkillManager.skill_levels.get(skill_id, 0)]
		else:
			btn.text = "(空)"
		btn.custom_minimum_size = Vector2(80, 35)
		equipped_container.add_child(btn)

	# Skill list
	var all_skills = SkillManager.get_all_definitions()

	# Active skills section
	var active_header = Label.new()
	active_header.text = "== 主动技能 =="
	skill_list.add_child(active_header)

	for skill_id in all_skills:
		var skill: SkillResource = all_skills[skill_id]
		if skill.skill_type == Constants.SkillType.ACTIVE:
			_add_skill_entry(skill, skill_id)

	var passive_header = Label.new()
	passive_header.text = "== 被动技能 =="
	skill_list.add_child(passive_header)

	for skill_id in all_skills:
		var skill: SkillResource = all_skills[skill_id]
		if skill.skill_type == Constants.SkillType.PASSIVE:
			_add_skill_entry(skill, skill_id)


func _add_skill_entry(skill: SkillResource, skill_id: StringName) -> void:
	var level: int = SkillManager.skill_levels.get(skill_id, 0)
	var hbox = HBoxContainer.new()

	var name_label = Label.new()
	var color = Color.WHITE if level > 0 else Color.GRAY
	name_label.add_theme_color_override("font_color", color)

	if level > 0:
		name_label.text = "%s Lv.%d/%d" % [skill.name, level, skill.max_level]
	else:
		name_label.text = "%s (未学习)" % skill.name
	name_label.custom_minimum_size = Vector2(180, 30)
	hbox.add_child(name_label)

	var desc_label = Label.new()
	desc_label.text = skill.description
	desc_label.add_theme_color_override("font_color", Color.LIGHT_GRAY)
	desc_label.custom_minimum_size = Vector2(200, 30)
	hbox.add_child(desc_label)

	var btn = Button.new()
	if level >= skill.max_level:
		btn.text = "已满级"
		btn.disabled = true
	elif level == 0:
		btn.text = "学习"
	else:
		btn.text = "升级"
	btn.custom_minimum_size = Vector2(60, 30)
	var sid = skill_id
	btn.pressed.connect(func(): SkillManager.upgrade_skill(sid))
	hbox.add_child(btn)

	# Equip button for active skills
	if skill.skill_type == Constants.SkillType.ACTIVE and level > 0:
		var eq_btn = Button.new()
		eq_btn.text = "装备"
		eq_btn.custom_minimum_size = Vector2(50, 30)
		for i in Constants.MAX_EQUIPPED_SKILLS:
			if SkillManager.equipped_skills[i] == skill_id:
				eq_btn.text = "已装"
				eq_btn.disabled = true
				break
		eq_btn.pressed.connect(func():
			for i in Constants.MAX_EQUIPPED_SKILLS:
				if SkillManager.equipped_skills[i] == &"":
					SkillManager.equip_active_skill(sid, i)
					break
			_refresh()
		)
		hbox.add_child(eq_btn)

	skill_list.add_child(hbox)
