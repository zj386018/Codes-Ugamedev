extends Node

# Placeholder audio manager - sounds would be loaded from files
var music_volume: float = 0.8
var sfx_volume: float = 1.0


func play_sfx(_sfx_name: String) -> void:
	# TODO: Load and play sound effects
	pass


func play_bgm(_bgm_name: String) -> void:
	# TODO: Load and play background music
	pass


func stop_bgm() -> void:
	pass


func serialize() -> Dictionary:
	return {
		"music_volume": music_volume,
		"sfx_volume": sfx_volume,
	}


func deserialize(data: Dictionary) -> void:
	music_volume = data.get("music_volume", 0.8)
	sfx_volume = data.get("sfx_volume", 1.0)
