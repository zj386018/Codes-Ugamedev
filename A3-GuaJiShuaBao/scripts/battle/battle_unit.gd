extends Node2D

@export var is_player: bool = true

var _shake_offset: Vector2 = Vector2.ZERO
var _shake_timer: float = 0.0
var _bounce_amount: float = 0.0
var _dead: bool = false

@onready var body: ColorRect = $Body
@onready var eye_left: ColorRect = $EyeLeft
@onready var eye_right: ColorRect = $EyeRight
@onready var pupil_left: ColorRect = $PupilLeft
@onready var pupil_right: ColorRect = $PupilRight
@onready var name_label: Label = $NameLabel
@onready var hp_bar: ProgressBar = $HPBar
@onready var hp_label: Label = $HPLabel


func _ready() -> void:
	if is_player:
		_setup_player()
	else:
		_setup_monster()


func _setup_player() -> void:
	body.color = Color(0.2, 0.5, 0.9)
	body.size = Vector2(60, 70)
	body.position = Vector2(-30, -35)
	body.position.y = -35

	eye_left.position = Vector2(-15, -25)
	eye_right.position = Vector2(5, -25)
	pupil_left.position = Vector2(-11, -21)
	pupil_right.position = Vector2(9, -21)

	name_label.text = "勇者"
	name_label.position = Vector2(-30, -55)


func _setup_monster() -> void:
	body.color = Color.GREEN
	body.size = Vector2(60, 60)
	body.position = Vector2(-30, -30)

	eye_left.position = Vector2(-15, -20)
	eye_right.position = Vector2(5, -20)
	pupil_left.position = Vector2(-11, -16)
	pupil_right.position = Vector2(9, -16)


func setup_monster(monster: MonsterResource) -> void:
	var s = monster.size
	body.color = monster.color
	body.size = Vector2(60 * s, 60 * s)
	body.position = Vector2(-30 * s, -30 * s)

	eye_left.size = Vector2(12 * s, 14 * s)
	eye_left.position = Vector2(-15 * s, -20 * s)
	eye_right.size = Vector2(12 * s, 14 * s)
	eye_right.position = Vector2(5 * s, -20 * s)
	pupil_left.size = Vector2(6 * s, 6 * s)
	pupil_left.position = Vector2(-11 * s, -16 * s)
	pupil_right.size = Vector2(6 * s, 6 * s)
	pupil_right.position = Vector2(9 * s, -16 * s)

	name_label.text = monster.display_name
	name_label.position = Vector2(-40, -45 * s)

	if monster.is_boss:
		# Boss gets a crown indicator
		name_label.add_theme_color_override("font_color", Color.GOLD)


func update_hp(current: int, maximum: int) -> void:
	if maximum <= 0:
		return
	hp_bar.max_value = maximum
	hp_bar.value = current
	hp_label.text = "%d/%d" % [current, maximum]


func play_attack() -> void:
	# Simple attack animation - bounce forward
	_bounce_amount = 20.0
	var tween = create_tween()
	if is_player:
		tween.tween_property(self, "position:x", position.x + 20, 0.15)
		tween.tween_property(self, "position:x", position.x, 0.15)
	else:
		tween.tween_property(self, "position:x", position.x - 20, 0.15)
		tween.tween_property(self, "position:x", position.x, 0.15)


func play_hurt() -> void:
	_shake_timer = 0.3
	# Flash red
	var original_color = body.color
	body.color = Color(1.0, 0.3, 0.3)
	var tween = create_tween()
	tween.tween_property(body, "color", original_color, 0.3)


func play_death() -> void:
	_dead = true
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 0.0, 0.5)
	await tween.finished
	modulate.a = 1.0
	_dead = false


func play_spawn() -> void:
	modulate.a = 0.0
	scale = Vector2(0.1, 0.1)
	var tween = create_tween()
	tween.set_parallel(true)
	tween.tween_property(self, "modulate:a", 1.0, 0.3)
	tween.tween_property(self, "scale", Vector2.ONE, 0.3).set_trans(Tween.TRANS_BACK)


func _process(delta: float) -> void:
	if _shake_timer > 0:
		_shake_timer -= delta
		_shake_offset = Vector2(randf_range(-3, 3), randf_range(-3, 3))
	else:
		_shake_offset = Vector2.ZERO
	position += _shake_offset
