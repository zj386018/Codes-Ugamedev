class_name Constants

enum Rarity { COMMON, UNCOMMON, RARE, EPIC, LEGENDARY }
enum EquipSlot { WEAPON, ARMOR, HELMET, BOOTS, ACCESSORY }
enum SkillType { ACTIVE, PASSIVE }
enum BuildingType { GOLD_MINE, XP_SHRINE, BLACKSMITH, TRAINING_GROUND }
enum Stat { NONE, HP, ATK, DEF, SPD, CRIT_RATE, CRIT_DMG }
enum GameState { MENU, PLAYING, PAUSED }

# Rarity colors (cartoon theme)
const RARITY_COLORS: Dictionary = {
	Rarity.COMMON: Color(0.9, 0.9, 0.9),
	Rarity.UNCOMMON: Color(0.3, 0.9, 0.3),
	Rarity.RARE: Color(0.3, 0.6, 1.0),
	Rarity.EPIC: Color(0.7, 0.3, 0.9),
	Rarity.LEGENDARY: Color(1.0, 0.85, 0.0),
}

const RARITY_NAMES: Dictionary = {
	Rarity.COMMON: "普通",
	Rarity.UNCOMMON: "优秀",
	Rarity.RARE: "稀有",
	Rarity.EPIC: "史诗",
	Rarity.LEGENDARY: "传说",
}

const SLOT_NAMES: Dictionary = {
	EquipSlot.WEAPON: "武器",
	EquipSlot.ARMOR: "护甲",
	EquipSlot.HELMET: "头盔",
	EquipSlot.BOOTS: "鞋子",
	EquipSlot.ACCESSORY: "饰品",
}

# Player base stats
const BASE_PLAYER_HP: int = 100
const BASE_PLAYER_ATK: int = 10
const BASE_PLAYER_DEF: int = 5
const BASE_PLAYER_SPD: int = 5
const BASE_CRIT_RATE: float = 0.05
const BASE_CRIT_DMG: float = 1.5

# Leveling
const XP_TO_LEVEL_BASE: int = 100
const XP_TO_LEVEL_GROWTH: float = 1.15
const STAT_PER_LEVEL: int = 3
const SKILL_POINT_PER_LEVEL: int = 1

# Combat
const BATTLE_TICK_RATE: float = 1.0
const MAX_EQUIPPED_SKILLS: int = 4

# Economy
const SELL_PRICE_MULTIPLIER: float = 0.3

# Buildings
const BUILDING_COST_GROWTH: float = 1.5
const BUILDING_OUTPUT_GROWTH: float = 1.2

# Offline
const OFFLINE_EFFICIENCY: float = 0.5
const MAX_OFFLINE_HOURS: float = 24.0

# Save
const AUTO_SAVE_INTERVAL: float = 60.0

# Stat allocation per point
const HP_PER_POINT: int = 15
const ATK_PER_POINT: int = 3
const DEF_PER_POINT: int = 2
const SPD_PER_POINT: float = 1.0
const CRIT_RATE_PER_POINT: float = 0.01
const CRIT_DMG_PER_POINT: float = 0.05
