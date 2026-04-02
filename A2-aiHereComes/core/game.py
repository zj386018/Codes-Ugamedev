import random
import pygame
from enum import Enum, auto
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, MAP_WIDTH, MAP_HEIGHT,
                       TILE_SIZE, Color, get_font)
from core.camera import Camera
from core.input import InputHandler
from world.map_generator import MapGenerator
from rendering.renderer import Renderer
from rendering.effects import ScreenEffects
from systems.resource_manager import ResourceManager
from systems.build_system import BuildSystem
from systems.pathfinding import Pathfinder
from systems.combat_system import CombatSystem
from systems.particle_system import ParticleSystem
from systems.wave_manager import WaveManager, WaveState
from save.save_manager import SaveManager
from entities.buildings.town_center import TownCenter
from entities.building import Building
from entities.zombie import Zombie
from ui.hud import HUD
from ui.build_panel import BuildPanel
from ui.notification import NotificationManager
from ui.info_panel import InfoPanel


class GamePhase(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Zombie Colony - Tower Defense Survival")
        self.clock = pygame.time.Clock()
        self.running = True
        self.phase = GamePhase.MENU

        # Systems (initialized in _start_new_game)
        self.camera = None
        self.input = None
        self.renderer = None
        self.game_map = None
        self.resource_manager = None
        self.build_system = None
        self.pathfinder = None
        self.combat_system = None
        self.particle_system = None
        self.zombies = None
        self.wave_manager = None
        self.hud = None
        self.build_panel = None
        self.notification = None
        self.town_center = None
        self.game_speed = 1.0
        self.screen_effects = ScreenEffects()
        self.info_panel = InfoPanel()
        self._notified_prep_times = set()

        # Fonts
        self.title_font = get_font(64)
        self.menu_font = get_font(36)
        self.small_font = get_font(22)

    def _start_new_game(self):
        """Initialize all game systems for a new game."""
        self.phase = GamePhase.PLAYING
        self.game_speed = 1.0

        # Core
        self.camera = Camera()
        self.input = InputHandler()
        self.renderer = Renderer(self.screen)
        self.game_map = MapGenerator().generate()

        # Economy
        self.resource_manager = ResourceManager()
        self.build_system = BuildSystem(self.game_map, self.resource_manager)

        # Town Center
        tc_x = MAP_WIDTH // 2 - 1
        tc_y = MAP_HEIGHT // 2 - 1
        self.town_center = TownCenter(tc_x, tc_y)
        self.town_center.place_on_map(self.game_map)
        self.build_system.buildings.append(self.town_center)
        self.build_system._apply_bonuses(self.town_center)

        # Combat
        self.pathfinder = Pathfinder(self.game_map)
        self.pathfinder.set_goal(tc_x + 1, tc_y + 1)
        self.combat_system = CombatSystem()
        self.particle_system = ParticleSystem()
        self.zombies = []

        # Waves
        self.wave_manager = WaveManager()

        # UI
        self.hud = HUD(self.resource_manager)
        self.build_panel = BuildPanel(self._on_building_selected,
                                         on_repair=self._on_repair_all)
        self.notification = NotificationManager()
        self.info_panel = InfoPanel()
        self.info_panel.on_upgrade = self._on_upgrade_building
        self.screen_effects = ScreenEffects()

        # Center camera
        tc_center_x = (tc_x + 1.5) * TILE_SIZE
        tc_center_y = (tc_y + 1.5) * TILE_SIZE
        self.camera.center_on(tc_center_x, tc_center_y)

        self.notification.show("欢迎！在第一波僵尸到来之前建造防御工事！", 5.0)

    def _on_building_selected(self, building_type):
        if building_type:
            self.build_system.select_building(building_type)
        else:
            self.build_system.deselect()

    def _on_repair_all(self):
        count, hp = self.build_system.repair_all()
        if count > 0:
            self.notification.show(f"已修复 {count} 个建筑！恢复 {hp} 生命值",
                                   2.0, (100, 200, 100))
            self.screen_effects.shake(amount=2.0, duration=0.15)
        else:
            self.notification.show("所有建筑状态良好", 1.5, (200, 200, 100))

    def _on_upgrade_building(self):
        entity = self.info_panel.selected
        if not isinstance(entity, Building) or not entity.can_upgrade():
            return
        cost = entity.get_upgrade_cost()
        if not self.resource_manager.can_afford(cost):
            self.notification.show("资源不足，无法升级！", 2.0, (200, 100, 100))
            return
        self.resource_manager.spend(cost)
        entity.upgrade()
        self.notification.show(
            f"{entity.name} 升级到 Lv{entity.level}！", 2.0, (255, 220, 50))
        self.screen_effects.shake(amount=2.0, duration=0.1)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)

            if not self._handle_events():
                break

            self._update(dt)
            self._render()

        pygame.quit()

    def _handle_events(self) -> bool:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                return False

        if self.phase == GamePhase.MENU:
            return self._handle_menu_events(events)
        elif self.phase == GamePhase.PLAYING:
            return self._handle_play_events(events)
        elif self.phase == GamePhase.PAUSED:
            return self._handle_pause_events(events)
        elif self.phase in (GamePhase.GAME_OVER, GamePhase.VICTORY):
            return self._handle_end_events(events)

        return True

    def _handle_menu_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self._start_new_game()
                elif event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if click is in the "New Game" button area
                mx, my = event.pos
                btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 400, 200, 50)
                if btn_rect.collidepoint(mx, my):
                    self._start_new_game()
        return True

    def _handle_play_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.phase = GamePhase.PAUSED
                return True

        self.input.process_events(events, self.camera)

        for event in events:
            if self.build_panel.handle_event(event):
                continue
            if self.info_panel.handle_event(event):
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.build_system.selected_building_type:
                    if event.pos[1] < SCREEN_HEIGHT - self.build_panel.panel_height:
                        tx, ty = self.input.mouse_tile
                        placed = self.build_system.place_building(
                            tx, ty, self.build_system.selected_building_type)
                        if placed:
                            self.pathfinder.invalidate()
                elif event.button == 1 and not self.build_system.selected_building_type:
                    # Click to select entity
                    if event.pos[1] < SCREEN_HEIGHT - self.build_panel.panel_height:
                        self._try_select_entity()
                if event.button == 3:
                    self.build_system.deselect()
                    self.build_panel.deselect()

            if event.type == pygame.KEYDOWN:
                key_map = {
                    pygame.K_1: "wall", pygame.K_2: "wood_tower",
                    pygame.K_3: "stone_tower", pygame.K_4: "farm",
                    pygame.K_5: "house", pygame.K_6: "storage",
                    pygame.K_7: "lumber_mill", pygame.K_8: "quarry",
                    pygame.K_9: "gold_mine",
                }
                if event.key in key_map:
                    bt = key_map[event.key]
                    if self.build_system.selected_building_type == bt:
                        self.build_system.deselect()
                        self.build_panel.deselect()
                    else:
                        self.build_system.select_building(bt)
                        self.build_panel.selected = bt
                        self.build_panel._update_button_states()

                # Debug: Z to spawn test zombies
                if event.key == pygame.K_z:
                    self._spawn_test_zombies()

                # Speed control
                if event.key == pygame.K_f:
                    self.game_speed = 2.0 if self.game_speed == 1.0 else 1.0
                    self.notification.show(
                        f"速度: {self.game_speed}x", 1.0)

                # Save/Load
                if event.key == pygame.K_F5:
                    SaveManager.save_game(SaveManager.build_save_state(self))
                    self.notification.show("游戏已保存！", 2.0, (100, 200, 100))
                if event.key == pygame.K_F9:
                    state = SaveManager.load_game()
                    if state:
                        self.notification.show("存档已加载（需重启）", 2.0, (200, 200, 100))
                    else:
                        self.notification.show("未找到存档", 2.0, (200, 100, 100))

        return True

    def _handle_pause_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    self.phase = GamePhase.PLAYING
                elif event.key == pygame.K_q:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Resume button
                if pygame.Rect(SCREEN_WIDTH // 2 - 100, 320, 200, 45).collidepoint(mx, my):
                    self.phase = GamePhase.PLAYING
                # Quit button
                elif pygame.Rect(SCREEN_WIDTH // 2 - 100, 380, 200, 45).collidepoint(mx, my):
                    return False
        return True

    def _handle_end_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._start_new_game()
                elif event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_m:
                    self.phase = GamePhase.MENU
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Restart button
                if pygame.Rect(SCREEN_WIDTH // 2 - 100, 400, 200, 45).collidepoint(mx, my):
                    self._start_new_game()
                # Menu button
                elif pygame.Rect(SCREEN_WIDTH // 2 - 100, 460, 200, 45).collidepoint(mx, my):
                    self.phase = GamePhase.MENU
        return True

    def _spawn_test_zombies(self):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x, y = random.uniform(0, MAP_WIDTH * TILE_SIZE), 0
        elif side == "bottom":
            x, y = random.uniform(0, MAP_WIDTH * TILE_SIZE), (MAP_HEIGHT - 1) * TILE_SIZE
        elif side == "left":
            x, y = 0, random.uniform(0, MAP_HEIGHT * TILE_SIZE)
        else:
            x, y = (MAP_WIDTH - 1) * TILE_SIZE, random.uniform(0, MAP_HEIGHT * TILE_SIZE)
        for _ in range(5):
            z = Zombie(
                x + random.uniform(-50, 50),
                y + random.uniform(-50, 50), "basic")
            z.goal_x = self.town_center.center[0]
            z.goal_y = self.town_center.center[1]
            self.zombies.append(z)

    def _try_select_entity(self):
        """Try to select a building or zombie at the mouse position."""
        wx, wy = self.input.mouse_world
        mx, my = int(wx), int(wy)

        # Check buildings
        for building in self.build_system.buildings:
            if building.rect.collidepoint(mx, my):
                self.info_panel.select(building)
                return

        # Check zombies
        for zombie in self.zombies:
            if zombie.rect.collidepoint(mx, my):
                self.info_panel.select(zombie)
                return

        # Nothing found
        self.info_panel.deselect()

    def _update(self, dt: float):
        if self.phase == GamePhase.PLAYING:
            self._update_game(dt * self.game_speed)
        self.screen_effects.update(dt)
        if self.notification:
            self.notification.update(dt)

    def _update_game(self, dt: float):
        # Camera
        dx, dy = self.input.get_camera_movement(dt / self.game_speed)
        self.camera.move(dx, dy)

        # Ghost
        self.build_system.update_ghost(*self.input.mouse_tile)

        # Buildings
        self.build_system.update(dt)

        # Wave management
        spawns = self.wave_manager.update(dt)
        hp_mult, dmg_mult = self.wave_manager.get_difficulty_multiplier()
        for zombie_type, sx, sy in spawns:
            z = Zombie(sx, sy, zombie_type)
            z.max_hp = int(z.max_hp * hp_mult)
            z.hp = z.max_hp
            z.damage = int(z.damage * dmg_mult)
            z.goal_x = self.town_center.center[0]
            z.goal_y = self.town_center.center[1]
            self.zombies.append(z)

        # Check wave complete
        if self.wave_manager.state == WaveState.ACTIVE:
            if len(self.wave_manager.spawn_queue) == 0 and len(self.zombies) == 0:
                self.wave_manager.check_wave_complete(0)
                if self.wave_manager.state == WaveState.PREP:
                    self.notification.show(
                        f"第 {self.wave_manager.current_wave} 波已清除！", 3.0,
                        (0, 255, 100))

        # Prep timer notification (only once per countdown milestone)
        if self.wave_manager.state == WaveState.PREP:
            prep = self.wave_manager.prep_timer
            wave_key = (self.wave_manager.current_wave + 1, 30)
            if prep <= 30 and wave_key not in self._notified_prep_times:
                self._notified_prep_times.add(wave_key)
                self.notification.show(
                    f"第 {self.wave_manager.current_wave + 1} 波还有 30 秒！",
                    2.0, (255, 200, 50))
        else:
            self._notified_prep_times.clear()

        # Zombies
        buildings = self.build_system.buildings
        for zombie in self.zombies:
            zombie.update(dt, self.pathfinder, self.game_map, buildings)

        # Combat
        self.combat_system.update(dt, buildings, self.zombies)

        # Handle zombie deaths
        for zombie in self.zombies:
            if not zombie.alive:
                self.particle_system.emit(zombie.center[0], zombie.center[1],
                                          count=6, color=(180, 0, 0))
                self.wave_manager.on_zombie_killed()
        self.zombies = [z for z in self.zombies if z.alive]

        # Handle building deaths
        for building in self.build_system.buildings[:]:
            if not building.alive:
                self.particle_system.emit(building.center[0], building.center[1],
                                          count=10, color=(150, 100, 50))
                self.build_system.remove_building(building)
                self.pathfinder.invalidate()
                self.screen_effects.shake(amount=4.0, duration=0.2)

                # Check town center destruction
                if isinstance(building, TownCenter):
                    self.screen_effects.shake(amount=10.0, duration=0.5)
                    self.phase = GamePhase.GAME_OVER
                    self.notification.show("城镇中心被摧毁！游戏结束！", 5.0,
                                           (255, 50, 50))

        # Particles
        self.particle_system.update(dt)

        # HUD
        self.hud.zombie_count = len(self.zombies)

        # Victory check
        if self.wave_manager.is_victory():
            self.phase = GamePhase.VICTORY
            self.notification.show("胜利！你存活了所有波次！", 5.0,
                                   (0, 255, 100))

    def _render(self):
        self.screen.fill(Color.BLACK)

        if self.phase == GamePhase.MENU:
            self._render_menu()
        elif self.phase == GamePhase.PAUSED:
            self._render_game()
            self._render_pause_overlay()
        elif self.phase in (GamePhase.GAME_OVER, GamePhase.VICTORY):
            self._render_game()
            self._render_end_overlay()
        else:
            self._render_game()

        # Notifications (always on top)
        if self.notification and self.phase != GamePhase.MENU:
            self.notification.draw(self.screen, SCREEN_WIDTH)

        pygame.display.flip()

    def _render_game(self):
        # Terrain
        self.renderer._render_terrain(self.game_map, self.camera)

        # Buildings
        for building in self.build_system.buildings:
            building.draw(self.screen, self.camera)

        # Ghost
        if self.phase == GamePhase.PLAYING:
            self.build_system.draw_ghost(self.screen, self.camera)

        # Zombies
        for zombie in self.zombies:
            zombie.draw(self.screen, self.camera)

        # Projectiles
        self.combat_system.draw(self.screen, self.camera)

        # Particles
        self.particle_system.draw(self.screen, self.camera)

        # Minimap
        self.renderer._render_minimap(self.game_map, self.camera,
                                      self.build_system.buildings, self.zombies)

        # HUD
        self.hud.draw(self.screen)

        # Wave info
        wave_text = self.wave_manager.get_prep_time_str()
        if wave_text:
            wave_surf = self.small_font.render(wave_text, True, Color.UI_TEXT)
            self.screen.blit(wave_surf, (SCREEN_WIDTH // 2 - wave_surf.get_width() // 2, 35))

        # Build panel
        self.build_panel.draw(self.screen, SCREEN_HEIGHT)

        # FPS & controls
        info = f"FPS:{int(self.clock.get_fps())} Speed:{self.game_speed}x  Wave:{self.wave_manager.current_wave}"
        info_surf = self.small_font.render(info, True, Color.WHITE)
        self.screen.blit(info_surf, (SCREEN_WIDTH - info_surf.get_width() - 10, SCREEN_HEIGHT - 75))

        # Info panel (selected entity)
        self.info_panel.draw(self.screen, self.camera)

        # Screen effects (shake)
        self.screen_effects.apply(self.screen)

    def _render_menu(self):
        # Title
        title = self.title_font.render("僵尸来了", True, (200, 50, 50))
        self.screen.blit(title,
                         (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

        subtitle = self.menu_font.render("塔防生存建造", True, Color.UI_TEXT)
        self.screen.blit(subtitle,
                         (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 230))

        # New Game button
        btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 400, 200, 50)
        pygame.draw.rect(self.screen, Color.UI_BUTTON, btn_rect)
        pygame.draw.rect(self.screen, Color.UI_BORDER, btn_rect, 2)
        btn_text = self.menu_font.render("开始游戏", True, Color.UI_TEXT)
        self.screen.blit(btn_text,
                         (btn_rect.centerx - btn_text.get_width() // 2,
                          btn_rect.centery - btn_text.get_height() // 2))

        # Controls info
        controls = [
            "WASD / 方向键: 滚动地图  |  鼠标边缘: 滚动地图",
            "1-9: 选择建筑  |  左键: 放置  |  右键: 取消",
            "F: 切换速度  |  ESC: 暂停  |  Z: 生成僵尸(调试)",
        ]
        y = 500
        for line in controls:
            surf = self.small_font.render(line, True, Color.GRAY)
            self.screen.blit(surf, (SCREEN_WIDTH // 2 - surf.get_width() // 2, y))
            y += 25

    def _render_pause_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        title = self.title_font.render("暂停", True, Color.UI_TEXT)
        self.screen.blit(title,
                         (SCREEN_WIDTH // 2 - title.get_width() // 2, 250))

        # Resume button
        btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, 320, 200, 45)
        pygame.draw.rect(self.screen, Color.UI_BUTTON, btn)
        pygame.draw.rect(self.screen, Color.UI_BORDER, btn, 2)
        txt = self.menu_font.render("继续", True, Color.UI_TEXT)
        self.screen.blit(txt, (btn.centerx - txt.get_width() // 2, btn.centery - txt.get_height() // 2))

        # Quit button
        btn2 = pygame.Rect(SCREEN_WIDTH // 2 - 100, 380, 200, 45)
        pygame.draw.rect(self.screen, Color.UI_BUTTON, btn2)
        pygame.draw.rect(self.screen, Color.UI_BORDER, btn2, 2)
        txt2 = self.menu_font.render("退出", True, Color.UI_TEXT)
        self.screen.blit(txt2, (btn2.centerx - txt2.get_width() // 2, btn2.centery - txt2.get_height() // 2))

    def _render_end_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        if self.phase == GamePhase.VICTORY:
            title = self.title_font.render("胜利!", True, (0, 255, 100))
        else:
            title = self.title_font.render("游戏结束", True, (255, 50, 50))
        self.screen.blit(title,
                         (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))

        # Stats
        if self.wave_manager:
            stats = [
                f"存活波数: {self.wave_manager.current_wave}",
                f"击杀僵尸: {self.wave_manager.total_zombies_killed}",
            ]
            y = 300
            for stat in stats:
                surf = self.menu_font.render(stat, True, Color.UI_TEXT)
                self.screen.blit(surf, (SCREEN_WIDTH // 2 - surf.get_width() // 2, y))
                y += 40

        # Buttons
        for i, (label, y) in enumerate([("重新开始", 400), ("主菜单", 460)]):
            btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, y, 200, 45)
            pygame.draw.rect(self.screen, Color.UI_BUTTON, btn)
            pygame.draw.rect(self.screen, Color.UI_BORDER, btn, 2)
            txt = self.menu_font.render(label, True, Color.UI_TEXT)
            self.screen.blit(txt, (btn.centerx - txt.get_width() // 2, btn.centery - txt.get_height() // 2))
