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
    def __init__(self, group):
        self._layer = 0
        super().__init__(100, "down", 100, "idle", group)
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
        self.WalkFrames = {"up":[WalkFrameData[16:20]],
                           "down":[WalkFrameData[0:4]],
                           "DownRight":[WalkFrameData[4:8]],
                           "Right":[WalkFrameData[8:12]],
                           "UpRight":[WalkFrameData[12:16]],
                           "DownLeft":[py.transform.flip(frame, False, True) for frame in [WalkFrameData[4:8]]],
                           "UpLeft":[py.transform.flip(frame, False, True) for frame in [WalkFrameData[12:16]]],
                           "Left":[py.transform.flip(frame, False, True) for frame in [WalkFrameData[8:12]]]}
        PunchFrameData = Sheets("Images/16x16 Attack-Sheet.png", "Images/16x16 Attack.json")
        self.PunchFrames = {"up":[PunchFrameData[24:30]],
                            "down":[PunchFrameData[0:6]],
                            "DownRight":[PunchFrameData[6:12]],
                            "Right":[PunchFrameData[12:18]],
                            "UpRight":[PunchFrameData[18:24]],
                            "DownLeft":[py.transform.flip(frame, False, True) for frame in [PunchFrameData[6:12]]],
                            "UpLeft":[py.transform.flip(frame, False, True) for frame in [PunchFrameData[18:24]]],
                            "Left":[py.transform.flip(frame, False, True) for frame in [PunchFrameData[12:18]]]}
        RunFrameData = Sheets("Images/16x16 Run-Sheet.png", "Images/16x16 Run.json")
        self.RunFrames = {"up":[RunFrameData[24:30]],
                            "down":[RunFrameData[0:6]],
                            "DownRight":[RunFrameData[6:12]],
                            "Right":[RunFrameData[12:18]],
                            "UpRight":[RunFrameData[18:24]],
                            "DownLeft":[py.transform.flip(frame, False, True) for frame in [RunFrameData[6:12]]],
                            "UpLeft":[py.transform.flip(frame, False, True) for frame in [RunFrameData[18:24]]],
                            "Left":[py.transform.flip(frame, False, True) for frame in [RunFrameData[12:18]]]}
        self.Directions = {(0,1):"down",
                           (0,-1):"up",
                           (1,1):"DownRight",
                           (1,-1):"UpRight",
                           (1,0):"Right",
                           (-1,0):"Left",
                           (-1,1):"DownLeft",
                           (-1,-1):"UpLeft"}
        self.animation_speed = 20
    
    def Walking(self, dt, FrameSet, keys):
        self.direction.x = int(keys[py.K_d] - keys[py.K_a])
        self.direction.y = int(keys[py.K_s] - keys[py.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        self.current_frame += self.animation_speed*dt
        if self.current_frame >= len(FrameSet):
            self.current_frame = 0
    
    def Compass(self, dt, Frameset):
        if self.direction:
            self.facing = self.Directions[(round(self.direction.x), round(self.direction.y))]
    def update(self, dt):
        
Pythong = Python(all_sprites)

while running:
    dt = clock.tick(60) / 1000
    Screen.fill('black')
    Screen.blit(bg, (0,0))
    all_sprites.update(dt)
    all_sprites.draw(Screen)
    py.display.flip()



