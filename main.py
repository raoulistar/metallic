import pygame as py
import random
import json
from Sprites.Player import Player
from Sprites.Guard import Guard
py.init()
ScreenHeight = 720
ScreenWidth = 1280
Screen = py.display.set_mode((ScreenWidth, ScreenHeight))
clock = py.Clock()
running = True
all_sprites = py.sprite.LayeredUpdates()
GuardGroup = py.sprite.Group()

Python = Player(all_sprites, ScreenWidth, ScreenHeight, GuardGroup)
Guard1 = Guard((all_sprites, GuardGroup), (ScreenWidth/3, ScreenHeight/2), Python)


while running:
    dt = clock.tick(60) / 1000
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    Screen.fill('blue')
    all_sprites.update(dt)
    for sprite in all_sprites:
        all_sprites.change_layer(sprite, sprite.rect.midbottom[1])
    all_sprites.draw(Screen)
    py.display.flip()
    print(type(all_sprites))
    print(all_sprites.get_layer_of_sprite(Python))



