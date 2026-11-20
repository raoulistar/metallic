import pygame as py
class JohnDoe(py.sprite.Sprite):
    def __init__(self, speed, facing, health, action, group):
        super().__init__(group)
        self.current_frame = 0
        self.speed = speed
        self.facing = facing
        self.direction = py.Vector2()
        self.health = health
        self.state = action
        self.has_been_hit = False