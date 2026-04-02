from typing import Set, Tuple, List
import pygame
from constants import CAMERA_SPEED, CAMERA_EDGE_SCROLL_ZONE, SCREEN_WIDTH, SCREEN_HEIGHT


class InputHandler:
    def __init__(self):
        self.keys_pressed: Set[int] = set()
        self.mouse_pos: Tuple[int, int] = (0, 0)
        self.mouse_world: Tuple[float, float] = (0.0, 0.0)
        self.mouse_tile: Tuple[int, int] = (0, 0)
        self.mouse_clicked_left = False
        self.mouse_clicked_right = False

    def process_events(self, events: List[pygame.event.Event], camera):
        """Process events from an external event list."""
        self.mouse_clicked_left = False
        self.mouse_clicked_right = False

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_clicked_left = True
                elif event.button == 3:
                    self.mouse_clicked_right = True
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

        # Update mouse world/tile position
        self.mouse_world = camera.screen_to_world(*self.mouse_pos)
        self.mouse_tile = camera.screen_to_tile(*self.mouse_pos)

    def get_camera_movement(self, dt: float) -> Tuple[float, float]:
        dx, dy = 0.0, 0.0

        # Keyboard
        if pygame.K_w in self.keys_pressed or pygame.K_UP in self.keys_pressed:
            dy -= CAMERA_SPEED * dt
        if pygame.K_s in self.keys_pressed or pygame.K_DOWN in self.keys_pressed:
            dy += CAMERA_SPEED * dt
        if pygame.K_a in self.keys_pressed or pygame.K_LEFT in self.keys_pressed:
            dx -= CAMERA_SPEED * dt
        if pygame.K_d in self.keys_pressed or pygame.K_RIGHT in self.keys_pressed:
            dx += CAMERA_SPEED * dt

        # Edge scroll
        mx, my = self.mouse_pos
        if mx < CAMERA_EDGE_SCROLL_ZONE:
            dx -= CAMERA_SPEED * dt
        elif mx > SCREEN_WIDTH - CAMERA_EDGE_SCROLL_ZONE:
            dx += CAMERA_SPEED * dt
        if my < CAMERA_EDGE_SCROLL_ZONE:
            dy -= CAMERA_SPEED * dt
        elif my > SCREEN_HEIGHT - CAMERA_EDGE_SCROLL_ZONE:
            dy += CAMERA_SPEED * dt

        return dx, dy
