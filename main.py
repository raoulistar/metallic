import pygame as py
import random
import json
py.init()
ScreenHeight = 1920
ScreenWidth = 1080
Screen = py.display.set_mode((ScreenWidth, ScreenHeight))
clock = py.Clock()
running = True
all_sprites = py.sprite.LayeredUpdates()

#base class for sprites
class JohnDoe(py.sprite.Sprite):
    def __init__(self, speed, facing, health, action):
        super().__init__()
        self.current_frame = 0
        self.speed = speed
        self.facing = facing
        self.direction = py.Vector2()
        self.health = health
        self.action = action
        self.has_been_hit = False

#Sprite Sheet Extraction function, no more manually coordinate grabbing hooray!

class Sheets():
    def __init__(self, image, jsonFile):
        self.SpriteSheet = py.image.load(image).convert_alpha()
        self.data = json.load((open(jsonFile)))
    def GetImage(self, x, y, w, h, scale):
        rect = py.Rect(x,y, w, h)
        image = self.sheet.subsurface(rect)
        image = py.transform.scale(image, (w*scale, h*scale))
        return image
    def ImageCoordinates(self, scale):
        Frames = []
        for frame in self.data["frames"].values():
            FrameData = frame["frame"]
            x = FrameData["x"]
            y = FrameData["y"]
            w = FrameData["w"]
            h = FrameData["h"]
            Frames.append(self.GetImage(x, y, w, h, scale))
        return Frames

class Python(JohnDoe):
    def __init__(self):
        self._layer = 10
        super().__init__(100, "down", 100, "idle")
        IdleFrameData = Sheets("Images/16x16 Idle-Sheet.png", "Images/16x16 Idle.json")
        self.IdleFrames = {"up":[IdleFrameData[16:20]],
                           "down":[IdleFrameData[0:4]],
                           "DownRight":[IdleFrameData[4:8]],
                           "Right":[IdleFrameData[8:12]],
                           "UpRight":[IdleFrameData[12:16]],
                           "DownLeft":[py.transform.flip(frame, False, True) for frame in [IdleFrameData[4:8]]],
                           "UpLeft":[py.transform.flip(frame, False, True) for frame in [IdleFrameData[12:16]]],
                           "Left":[py.transform.flip(frame, False, True) for frame in [IdleFrameData[8:12]]]}
        self.image = self.IdleFrames["down"][0]
        self.rect = self.image.get_frect(center = ((ScreenWidth/2), (ScreenHeight/4)))
        self.hurtbox = self.rect.inflate(-2, -2)
        WalkFrameData = Sheets("Images/16x16 Walk-Sheet.png", "Images/16x16 Walk.json")
        self.animation_speed = 20





