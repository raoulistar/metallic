import json
import pygame as py
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