extends Control

signal panel_changed(panel_name: String)

var _current_panel: String = ""
var _panel_history: Array[String] = []

@onready var battle_btn: Button = $BottomNav/BattleBtn
@onready var char_btn: Button = $BottomNav/CharBtn
@onready var inv_btn: Button = $BottomNav/InvBtn
@onready var skill_btn: Button = $BottomNav/SkillBtn
@onready var build_btn: Button = $BottomNav/BuildBtn
@onready var shop_btn: Button = $BottomNav/ShopBtn
@onready var setting_btn: Button = $BottomNav/SettingBtn

@onready var panels: Dictionary = {}

func _ready() -> void:
	# Store panel references
	panels = {
		"character": $PanelContainer/CharacterPanel,
		"inventory": $PanelContainer/InventoryPanel,
		"skill": $PanelContainer/SkillPanel,
		"building": $PanelContainer/BuildingPanel,
		"shop": $PanelContainer/ShopPanel,
		"settings": $PanelContainer/SettingsPanel,
	}

	# Hide all panels initially
	for panel_name in panels:
		panels[panel_name].visible = false

	# Connect navigation buttons
	battle_btn.pressed.connect(func(): _show_panel(""))
	char_btn.pressed.connect(func(): _show_panel("character"))
	inv_btn.pressed.connect(func(): _show_panel("inventory"))
	skill_btn.pressed.connect(func(): _show_panel("skill"))
	build_btn.pressed.connect(func(): _show_panel("building"))
	shop_btn.pressed.connect(func(): _show_panel("shop"))
	setting_btn.pressed.connect(func(): _show_panel("settings"))

	# Toast notifications
	NotificationManager.toast_requested.connect(_on_toast)


func _show_panel(panel_name: String) -> void:
	# Hide current panel
	if _current_panel != "" and panels.has(_current_panel):
		panels[_current_panel].visible = false

	_current_panel = panel_name

	# Show new panel
	if panel_name != "" and panels.has(panel_name):
		panels[panel_name].visible = true

	panel_changed.emit(panel_name)


func _on_toast(message: String) -> void:
	var toast = preload("res://scenes/ui/components/toast.tscn").instantiate()
	toast.message = message
	$ToastLayer.add_child(toast)
