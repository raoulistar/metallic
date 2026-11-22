import pygame as py
from Sprites.JohnDoe import JohnDoe
from OtherFunctions.SheetGrabbing import Sheets 
class Player(JohnDoe):
    def __init__(self, groups, ScreenWidth, ScreenHeight, guards):
        self._layer = 10
        super().__init__(100, "down", 100, "Idle", groups)
        self.scale = 4
        IdleFrameData = Sheets("Images/16x16 Idle-Sheet.png", "Images/16x16 Idle.json").ImageCoordinates(self.scale)
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
        WalkFrameData = Sheets("Images/16x16 Walk-Sheet.png", "Images/16x16 Walk.json").ImageCoordinates(self.scale)
        self.WalkFrames = {"up":WalkFrameData[16:20],
                           "down":WalkFrameData[0:4],
                           "DownRight":WalkFrameData[4:8],
                           "Right":WalkFrameData[8:12],
                           "UpRight":WalkFrameData[12:16],
                           "DownLeft":[py.transform.flip(frame, True, False) for frame in WalkFrameData[4:8]],
                           "UpLeft":[py.transform.flip(frame, True, False) for frame in WalkFrameData[12:16]],
                           "Left":[py.transform.flip(frame, True, False) for frame in WalkFrameData[8:12]]}
        PunchFrameData = Sheets("Images/16x16 Attack-Sheet.png", "Images/16x16 Attack.json").ImageCoordinates(self.scale)
        self.PunchFrames = {"up":PunchFrameData[24:30],
                            "down":PunchFrameData[0:6],
                            "DownRight":PunchFrameData[6:12],
                            "Right":PunchFrameData[12:18],
                            "UpRight":PunchFrameData[18:24],
                            "DownLeft":[py.transform.flip(frame, True, False) for frame in PunchFrameData[6:12]],
                            "UpLeft":[py.transform.flip(frame, True, False) for frame in PunchFrameData[18:24]],
                            "Left":[py.transform.flip(frame, True, False) for frame in PunchFrameData[12:18]]}
        RunFrameData = Sheets("Images/16x16 Run-Sheet.png", "Images/16x16 Run.json").ImageCoordinates(self.scale)
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
        self.Volume = {"Idle":(0,0),
                       "Walking":(5,75),
                       "Running":(50,200)}
        self.SoundMeter = 0
        self.GuardGroup = guards
        self.Evidence = py.Vector2()

    def SoundArea(self, dt):
        self.SoundMeter = self.Volume.get(self.state, 0)
        for sprite in self.GuardGroup:
            if py.Vector2(self.rect.center).distance_squared_to(sprite.rect.center) < (self.SoundMeter[1]**2):
                sprite.Alertness += self.SoundMeter[0]*dt
        if self.state == "Running":
            self.Evidence = self.rect.center


    def Walking(self, dt, FrameSet, keys):
        self.direction.x = int(keys[py.K_d] - keys[py.K_a])
        self.direction.y = int(keys[py.K_s] - keys[py.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * (self.speed*(1+(keys[py.K_LSHIFT]*1.5))) * dt
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
        self.SoundArea(dt)
        self.Walking(dt, CurrentFrameSet, keys)
        self.image = CurrentFrameSet[int(self.current_frame)]
        pass