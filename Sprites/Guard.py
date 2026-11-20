from Sprites.JohnDoe import JohnDoe
from OtherFunctions.SheetGrabbing import Sheets
import pygame as py
class Guard(JohnDoe):
    def __init__(self, groups, starting_pos, Python):
        self._layer = 0
        super().__init__(110, "right", 50, "idle", groups)
        self.scale = 3.5
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
        self.actions = {"Idle":self.IdleFrames,
                        "Walking":self.WalkFrames,
                        "Slashing":self.SlashFrames,
                        "Shooting":self.BowShotFrames,
                        "Hurt":self.HurtFrames,
                        "Dead":self.DeadFrames}
        self.radius = 5
        self.image = self.IdleFrames[self.facing][0]
        self.rect = self.image.get_frect(center = starting_pos)
        self.distance = py.Vector2(self.rect.center).distance_to(Python.rect.center)
        self.Alertness = 0

    def Chase(self, dt,):
        pass

    def update(self, dt):
        pass