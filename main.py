import pygame as py
import random
import json
py.init()
ScreenHeight = 720
ScreenWidth = 1280
Screen = py.display.set_mode((ScreenWidth, ScreenHeight))
clock = py.Clock()
running = True
all_sprites = py.sprite.Group()

#base class for sprites
class JohnDoe(py.sprite.Sprite):
    def __init__(self, speed, facing, health, action, group):
        super().__init__()
        self.current_frame = 0
        self.speed = speed
        self.facing = facing
        self.direction = py.Vector2()
        self.health = health
        self.state = action
        self.has_been_hit = False

#Sprite Sheet Extraction function, no more manually coordinate grabbing hooray!

class Sheets():
    def __init__(self, image, jsonFile):
        self.SpriteSheet = py.image.load(image).convert_alpha()
        self.data = json.load((open(jsonFile)))
    def GetImage(self, x, y, w, h, scale):
        rect = py.Rect(x,y, w, h)
        image = self.SpriteSheet.subsurface(rect)
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

class Player(JohnDoe):
    def __init__(self, groups, sheetloader:Sheets):
        self._layer = 0
        super().__init__(100, "down", 100, "Idle", groups)
        self.scale = 4
        IdleFrameData = sheetloader("Images/16x16 Idle-Sheet.png", "Images/16x16 Idle.json").ImageCoordinates(self.scale)
        self.IdleFrames = {"up":IdleFrameData[16:20],
                           "down":IdleFrameData[0:4],
                           "DownRight":IdleFrameData[4:8],
                           "Right":IdleFrameData[8:12],
                           "UpRight":IdleFrameData[12:16],
                           "DownLeft":[py.transform.flip(frame, True, False) for frame in IdleFrameData[4:8]],
                           "UpLeft":[py.transform.flip(frame, True, False) for frame in IdleFrameData[12:16]],
                           "Left":[py.transform.flip(frame, True, False) for frame in IdleFrameData[8:12]]}
        self.image = self.IdleFrames["down"][0]
        self.rect = self.image.get_frect(center = ((ScreenWidth/2), (ScreenHeight/4)))
        self.hurtbox = self.rect.inflate(-2, -2)
        WalkFrameData = sheetloader("Images/16x16 Walk-Sheet.png", "Images/16x16 Walk.json").ImageCoordinates(self.scale)
        self.WalkFrames = {"up":WalkFrameData[16:20],
                           "down":WalkFrameData[0:4],
                           "DownRight":WalkFrameData[4:8],
                           "Right":WalkFrameData[8:12],
                           "UpRight":WalkFrameData[12:16],
                           "DownLeft":[py.transform.flip(frame, True, False) for frame in WalkFrameData[4:8]],
                           "UpLeft":[py.transform.flip(frame, True, False) for frame in WalkFrameData[12:16]],
                           "Left":[py.transform.flip(frame, True, False) for frame in WalkFrameData[8:12]]}
        PunchFrameData = sheetloader("Images/16x16 Attack-Sheet.png", "Images/16x16 Attack.json").ImageCoordinates(self.scale)
        self.PunchFrames = {"up":PunchFrameData[24:30],
                            "down":PunchFrameData[0:6],
                            "DownRight":PunchFrameData[6:12],
                            "Right":PunchFrameData[12:18],
                            "UpRight":PunchFrameData[18:24],
                            "DownLeft":[py.transform.flip(frame, True, False) for frame in PunchFrameData[6:12]],
                            "UpLeft":[py.transform.flip(frame, True, False) for frame in PunchFrameData[18:24]],
                            "Left":[py.transform.flip(frame, True, False) for frame in PunchFrameData[12:18]]}
        RunFrameData = sheetloader("Images/16x16 Run-Sheet.png", "Images/16x16 Run.json").ImageCoordinates(self.scale)
        self.RunFrames = {"up":RunFrameData[24:30],
                            "down":RunFrameData[0:6],
                            "DownRight":RunFrameData[6:12],
                            "Right":RunFrameData[12:18],
                            "UpRight":RunFrameData[18:24],
                            "DownLeft":[py.transform.flip(frame, True, False) for frame in RunFrameData[6:12]],
                            "UpLeft":[py.transform.flip(frame, True, False) for frame in RunFrameData[18:24]],
                            "Left":[py.transform.flip(frame, True, False) for frame in RunFrameData[12:18]]}
        self.EightDirections = {(0,1):"down",
                           (0,-1):"up",
                           (1,1):"DownRight",
                           (1,-1):"UpRight",
                           (1,0):"Right",
                           (-1,0):"Left",
                           (-1,1):"DownLeft",
                           (-1,-1):"UpLeft"}
        self.actions = {"Walking": self.WalkFrames,
                        "Idle": self.IdleFrames,
                        "Attacking":self.PunchFrames,
                        "Running":self.RunFrames}
        self.animation_speed = 10
    
    def Walking(self, dt, FrameSet, keys):
        self.direction.x = int(keys[py.K_d] - keys[py.K_a])
        self.direction.y = int(keys[py.K_s] - keys[py.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * (self.speed*(1+(keys[py.K_LSHIFT]*2))) * dt
        self.current_frame += self.animation_speed*dt
        if self.current_frame >= len(FrameSet):
            self.current_frame = 0
    
    def Attacking(self, dt, Frameset):
        return
    
    def IndustrialStateMachine(self, keys, recentkeys):
        moving = ((keys[py.K_w] or keys[py.K_a] or keys[py.K_s] or keys[py.K_d]))
        if self.state != "Attacking":
            if moving:
                if keys[py.K_LSHIFT]:
                    self.state = "Running"
                else:
                    self.state = "Walking"
            elif recentkeys[py.K_o]:
                self.state = "Attacking"
            else:
                self.state = "Idle"
    def Compass(self):
        if self.direction and self.state != "Attacking":
            self.facing = self.EightDirections[(round(self.direction.x), round(self.direction.y))]
    def update(self, dt):
        recentkeys = py.key.get_just_pressed()
        keys = py.key.get_pressed()
        self.IndustrialStateMachine(keys, recentkeys)
        self.Compass()
        CurrentFrameSet = self.actions[self.state][self.facing]
        self.Walking(dt, CurrentFrameSet, keys)
        self.image = CurrentFrameSet[int(self.current_frame)]
        print(self.facing)
        print(self.state)
Python = Player(all_sprites, Sheets)

class Guard(JohnDoe):
    def __init__(self, groups):
        self._layer = 0
        super.__init__(110, "right", 50, "idle", groups)
        self.scale = 4
        self.AllFrameData = Sheets("Images/Soldier.png", "Images/Soldier.json").ImageCoordinates(self.scale)
        self.IdleFrames = {"right":self.AllFrameData[0:5],
                           "left":[py.transform.flip(frame, True, False) for frame in self.AllFrameData[0:5]]}
        self.WalkFrames = {"right":self.AllFrameData[6:13],
                           "left":[py.transform.flip(frame, True, False) for frame in self.AllFrameData[6:13]]}
        self.SlashFrames = {"right":self.AllFrameData[14:19],
                            "left":[py.transform.flip(frame, True, False) for frame in self.AllFrameData[14:19]]}
        self.JumpSlashFrames = {"right":self.AllFrameData[20:25],
                                "left":[py.transform.flip(frame, True, False) for frame in self.AllFrameData[20:25]]}
        self.BowShotFrames = {"right": self.AllFrameData[26:34],
                              "left":[py.transform.flip(frame, True, False) for frame in self.AllFrameData[26:34]]}
        self.HurtFrames = {"right":self.AllFrameData[35:38],
                           "left":[py.transform.flip(frame, True, False) for frame in self.AllFrameData[35:38]]}
        self.DeadFrames = {"right":self.AllFrameData[39:42],
                           "left":[py.transform.flip(frame, True, False) for frame in self.AllFrameData[39:42]]}
all_sprites.add(Python)
while running:
    dt = clock.tick(60) / 1000
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    Screen.fill('blue')
    all_sprites.update(dt)
    all_sprites.draw(Screen)
    py.display.flip()



