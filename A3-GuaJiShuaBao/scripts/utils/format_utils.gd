class_name FormatUtils

static func format_number(value: float) -> String:
	if value < 0:
		return "-" + format_number(-value)
	if value < 1000:
		return str(int(value))
	if value < 1_000_000:
		return "%.1fK" % (value / 1000.0)
	if value < 1_000_000_000:
		return "%.1fM" % (value / 1_000_000.0)
	if value < 1_000_000_000_000.0:
		return "%.1fB" % (value / 1_000_000_000.0)
	return "%.1fT" % (value / 1_000_000_000_000.0)


static func format_time(seconds: float) -> String:
	var secs = int(seconds) % 60
	var mins = (int(seconds) / 60) % 60
	var hours = int(seconds) / 3600
	if hours > 0:
		return "%d:%02d:%02d" % [hours, mins, secs]
	return "%d:%02d" % [mins, secs]


static func format_percent(value: float) -> String:
	return "%.1f%%" % (value * 100.0)


static func xp_to_next_level(level: int) -> int:
	return int(Constants.XP_TO_LEVEL_BASE * pow(Constants.XP_TO_LEVEL_GROWTH, level - 1))
