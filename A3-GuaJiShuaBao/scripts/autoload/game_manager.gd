extends Node

signal game_state_changed(new_state: int)

var game_state: int = Constants.GameState.MENU
var play_time: float = 0.0


func _ready() -> void:
	# Try to load existing save
	if SaveManager.has_save(0):
		if SaveManager.load_game(0):
			# Calculate offline rewards
			var rewards = SaveManager.calculate_offline_rewards()
			if rewards.gold > 0 or rewards.xp > 0:
				_show_offline_rewards(rewards)
		else:
			_new_game()
	else:
		_new_game()

	BattleManager.start_battle()
	game_state = Constants.GameState.PLAYING
	game_state_changed.emit(game_state)


func _process(delta: float) -> void:
	if game_state == Constants.GameState.PLAYING:
		play_time += delta


func _new_game() -> void:
	PlayerData.full_heal()
	EconomyManager.add_gold(50)


func _show_offline_rewards(rewards: Dictionary) -> void:
	# Apply offline rewards directly
	if rewards.gold > 0:
		EconomyManager.add_gold(rewards.gold)
	if rewards.xp > 0:
		PlayerData.add_experience(rewards.xp)
	# Could show a popup here - for now just apply them


func get_play_time() -> float:
	return play_time
