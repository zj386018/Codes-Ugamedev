# 游戏数据结构定义

class Scene:
    """游戏场景类"""
    def __init__(self, id, title, description, choices=None, items=None, requirements=None):
        self.id = id
        self.title = title
        self.description = description
        self.choices = choices or []  # 选择列表：[(text, next_scene_id), ...]
        self.items = items or []  # 可获得的物品
        self.requirements = requirements or []  # 进入场景的要求

class Item:
    """物品类"""
    def __init__(self, id, name, description, usable=False):
        self.id = id
        self.name = name
        self.description = description
        self.usable = usable  # 是否可以使用

class Player:
    """玩家类"""
    def __init__(self):
        self.health = 100
        self.max_health = 100
        self.inventory = []  # 物品ID列表
        self.current_scene = "start"
        self.game_flags = {}  # 游戏标志位

# 游戏场景数据
SCENES = {
    "start": Scene(
        "start",
        "神秘森林",
        "你醒来时发现自己身处一片神秘的森林中。四周弥漫着薄雾，远处传来奇怪的声音。你感到有些迷茫，但必须找到出路。",
        [
            ("沿着小径向前走", "forest_path"),
            ("检查周围的环境", "examine_area"),
            ("大声呼救", "call_for_help")
        ],
        [],
        []
    ),
    
    "forest_path": Scene(
        "forest_path",
        "森林小径",
        "你沿着一条蜿蜒的小径前进。路两旁的树木越来越密集，阳光透过树叶的缝隙洒下斑驳的光影。",
        [
            ("继续前进", "deep_forest"),
            ("返回起点", "start"),
            ("仔细观察路边", "check_roadside")
        ],
        ["树枝"],
        []
    ),
    
    "examine_area": Scene(
        "examine_area",
        "仔细观察",
        "你仔细观察周围，发现了一些有趣的细节。地上有一些奇怪的脚印，不远处似乎有一个山洞。",
        [
            ("跟随脚印", "follow_tracks"),
            ("探索山洞", "cave_entrance"),
            ("回到原点", "start")
        ],
        ["地图碎片"],
        []
    ),
    
    "call_for_help": Scene(
        "call_for_help",
        "呼救",
        "你大声呼救，声音在森林中回荡。突然，你听到了回应声，但似乎不是人类的声音...",
        [
            ("朝着声音方向前进", "mysterious_sound"),
            ("保持安静等待", "wait_quietly"),
            ("逃离这个方向", "run_away")
        ],
        [],
        []
    ),
    
    "deep_forest": Scene(
        "deep_forest",
        "森林深处",
        "你来到了森林深处，这里更加阴暗。前方有一座古老的小屋，看起来已经废弃很久了。",
        [
            ("进入小屋", "old_house"),
            ("绕过小屋继续前进", "bypass_house"),
            ("返回", "forest_path")
        ],
        ["生锈的钥匙"],
        []
    ),
    
    "check_roadside": Scene(
        "check_roadside",
        "路边发现",
        "在路边，你发现了一个破旧的背包，里面有一些有用的物品。",
        [
            ("拿走背包", "take_backpack"),
            ("继续前进", "deep_forest"),
            ("返回", "forest_path")
        ],
        ["急救包", "手电筒"],
        []
    ),
    
    "follow_tracks": Scene(
        "follow_tracks",
        "跟随脚印",
        "你跟着脚印前进，发现它们通向一个隐藏的营地。营地里有篝火的痕迹和一些生活用品。",
        [
            ("搜查营地", "search_camp"),
            ("继续跟踪脚印", "continue_tracking"),
            ("返回", "examine_area")
        ],
        ["露营刀", "罐头食品"],
        []
    ),
    
    "cave_entrance": Scene(
        "cave_entrance",
        "山洞入口",
        "你站在山洞入口，里面传来阵阵寒意。洞口有一些奇怪的符号，似乎在警告着什么。",
        [
            ("勇敢地进入", "inside_cave"),
            ("先在外面准备", "prepare_outside"),
            ("放弃探索", "examine_area")
        ],
        [],
        []
    ),
    
    "mysterious_sound": Scene(
        "mysterious_sound",
        "神秘声音",
        "你朝着声音的方向前进，发现了一只受伤的狼。它看起来很痛苦，但眼神中透露出一丝友善。",
        [
            ("帮助狼", "help_wolf"),
            ("小心地绕过", "avoid_wolf"),
            ("慢慢后退", "back_away")
        ],
        ["狼牙项链"],
        []
    ),
    
    "old_house": Scene(
        "old_house",
        "古老小屋",
        "你推开门进入小屋。里面布满灰尘，但似乎有人居住的痕迹。桌上有一本日记。",
        [
            ("阅读日记", "read_diary"),
            ("搜查房间", "search_room"),
            ("离开小屋", "deep_forest")
        ],
        ["神秘日记", "古老护身符"],
        []
    ),
    
    "inside_cave": Scene(
        "inside_cave",
        "山洞内部",
        "山洞内部比想象的要明亮，墙壁上有发光的苔藓。深处传来水滴声，似乎有地下河。",
        [
            ("探索深处", "cave_deep"),
            ("检查发光苔藓", "examine_moss"),
            ("离开山洞", "cave_entrance")
        ],
        ["发光苔藓", "水晶碎片"],
        []
    ),
    
    "help_wolf": Scene(
        "help_wolf",
        "帮助狼",
        "你小心翼翼地接近狼，用急救包为它处理伤口。狼感激地看着你，然后起身引你走向一个隐藏的地方。",
        [
            ("跟随狼", "follow_wolf"),
            ("感谢后离开", "thank_and_leave"),
            ("询问更多信息", "ask_wolf")
        ],
        ["狼的友谊"],
        []
    ),
    
    "cave_deep": Scene(
        "cave_deep",
        "山洞深处",
        "在山洞深处，你发现了一个地下湖泊。湖水清澈见底，湖中央有一个小岛，岛上有一座古老的祭坛。",
        [
            ("游向小岛", "swim_to_island"),
            ("在湖边搜索", "search_lakeside"),
            ("返回", "inside_cave")
        ],
        ["古老符文"],
        []
    ),
    
    "swim_to_island": Scene(
        "swim_to_island",
        "祭坛小岛",
        "你游到小岛上，发现祭坛上有一个发光的宝箱。当你靠近时，宝箱自动打开了。",
        [
            ("拿取宝物", "take_treasure"),
            ("研究祭坛", "study_altar"),
            ("返回", "cave_deep")
        ],
        ["神秘宝物"],
        []
    ),
    
    "ending_good": Scene(
        "ending_good",
        "完美结局",
        "恭喜你！你成功解开了森林的秘密，找到了传说中的宝藏。狼成为了你的忠实伙伴，你带着丰富的收获离开了这片神秘森林。",
        [],
        [],
        []
    ),
    
    "ending_bad": Scene(
        "ending_bad",
        "悲剧结局",
        "很遗憾，你在森林中迷失了方向，最终成为了森林的一部分。也许下一个冒险者会发现你的故事...",
        [],
        [],
        []
    )
}

# 物品数据
ITEMS = {
    "树枝": Item("树枝", "树枝", "一根结实的树枝，可以用作武器或工具", True),
    "地图碎片": Item("地图碎片", "地图碎片", "一张古老的地图碎片，似乎指向某个重要地点", False),
    "生锈的钥匙": Item("生锈的钥匙", "生锈的钥匙", "一把古老的钥匙，不知道能打开什么", True),
    "急救包": Item("急救包", "急救包", "可以恢复生命值的医疗用品", True),
    "手电筒": Item("手电筒", "手电筒", "可以在黑暗中照明的工具", True),
    "露营刀": Item("露营刀", "露营刀", "一把锋利的露营刀，很有用", True),
    "罐头食品": Item("罐头食品", "罐头食品", "可以充饥的食物", True),
    "狼牙项链": Item("狼牙项链", "狼牙项链", "一个神秘的狼牙项链，似乎有特殊力量", False),
    "神秘日记": Item("神秘日记", "神秘日记", "记录着森林秘密的古老日记", False),
    "古老护身符": Item("古老护身符", "古老护身符", "一个提供保护的神秘护身符", False),
    "发光苔藓": Item("发光苔藓", "发光苔藓", "可以在黑暗中发光的特殊苔藓", False),
    "水晶碎片": Item("水晶碎片", "水晶碎片", "美丽的水晶碎片，蕴含着神秘力量", False),
    "狼的友谊": Item("狼的友谊", "狼的友谊", "与狼建立的友谊，这是最珍贵的宝物", False),
    "古老符文": Item("古老符文", "古老符文", "记录着古老智慧的神秘符文", False),
    "神秘宝物": Item("神秘宝物", "神秘宝物", "传说中的神秘宝物，拥有无穷的力量", False)
}
