extends Control

@onready var timer_label: Label = $VBox/TimerLabel
@onready var item_list: VBoxContainer = $VBox/ScrollContainer/ItemList


func _ready() -> void:
	ShopManager.shop_refreshed.connect(_refresh)
	_refresh()


func _process(_delta: float) -> void:
	var remaining = ShopManager.get_refresh_time_remaining()
	timer_label.text = "下次刷新: %s" % FormatUtils.format_time(remaining)


func _refresh() -> void:
	for child in item_list.get_children():
		child.queue_free()

	var items = ShopManager.get_shop_items()
	for i in items.size():
		var item = items[i]
		var card = Panel.new()
		var hbox = HBoxContainer.new()

		var info = VBoxContainer.new()

		var name_label = Label.new()
		name_label.text = item.get("name", "")
		info.add_child(name_label)

		var desc_label = Label.new()
		desc_label.text = item.get("description", "")
		desc_label.add_theme_font_size_override("font_size", 12)
		desc_label.add_theme_color_override("font_color", Color.LIGHT_GRAY)
		info.add_child(desc_label)

		hbox.add_child(info)

		var spacer = Control.new()
		spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		hbox.add_child(spacer)

		var cost_label = Label.new()
		var currency = item.get("currency", "gold")
		var cost = item.get("cost", 0)
		if currency == "gold":
			cost_label.text = "%d 金币" % cost
		else:
			cost_label.text = "%d 宝石" % cost
		cost_label.add_theme_color_override("font_color", Color.GOLD if currency == "gold" else Color.CYAN)
		hbox.add_child(cost_label)

		var btn = Button.new()
		btn.text = "购买"
		btn.custom_minimum_size = Vector2(80, 40)
		var idx = i
		btn.pressed.connect(func(): _purchase(idx))
		hbox.add_child(btn)

		card.add_child(hbox)
		card.custom_minimum_size = Vector2(650, 70)
		item_list.add_child(card)


func _purchase(index: int) -> void:
	if ShopManager.purchase_item(index):
		NotificationManager.show_toast("购买成功!")
		_refresh()
	else:
		NotificationManager.show_toast("购买失败! 资源不足")
