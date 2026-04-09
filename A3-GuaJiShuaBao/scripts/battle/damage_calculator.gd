class_name DamageCalculator

static func compute_damage(attacker_atk: int, defender_def: int, crit_rate: float, crit_dmg: float, skill_multiplier: float = 1.0) -> Dictionary:
	var base_damage = attacker_atk * skill_multiplier
	var defense_reduction = defender_def / float(defender_def + 100.0)
	var damage = base_damage * (1.0 - defense_reduction)

	var is_crit = randf() < crit_rate
	if is_crit:
		damage *= crit_dmg

	damage = maxf(1.0, floorf(damage))
	return {"damage": int(damage), "is_crit": is_crit}
