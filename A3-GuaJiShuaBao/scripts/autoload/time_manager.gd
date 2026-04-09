extends Node

signal offline_duration_calculated(seconds: float)

var _last_timestamp: float = 0.0

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_last_timestamp = Time.get_unix_time_from_system()


func get_current_timestamp() -> float:
	return Time.get_unix_time_from_system()


func calculate_offline_time(saved_timestamp: float) -> float:
	var current = get_current_timestamp()
	var elapsed = current - saved_timestamp
	var max_seconds = Constants.MAX_OFFLINE_HOURS * 3600.0
	return minf(elapsed, max_seconds)


func get_play_time_string(seconds: float) -> String:
	return FormatUtils.format_time(seconds)
