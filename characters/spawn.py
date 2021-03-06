"""
Abby Nason
smash! the ceiling
spawn.py

Creates the boss blob spawns.
"""
import pygame
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.mobile import Mobile
import os
import random
from modules.frameManager import FRAMES

SPRITE_SIZE = Vector2(24, 40)
MAX_VELOCITY = 50
ACCELERATION = 5.0
ZAP_RANGE = 50

class Spawn(Mobile):

    def __init__(self, position, spriteSize):
        """initializes a spawn object"""
        position = Vector2(position.x - spriteSize.x//2, position.y)
        randomColor = random.randint(0,12)
        #randomizes the colors of the spawns
        if randomColor < 3:
            self._offsetX = 0
        elif randomColor < 6:
            self._offsetX = 1
        elif randomColor < 9:
            self._offsetX = 2
        else:
            self._offsetX = 3
        super().__init__("blob_spawns.png", position, (self._offsetX,0))
        #a vector2 of its velocity
        self._originalPosition = position
        self._velocity = Vector2(MAX_VELOCITY,MAX_VELOCITY)
        self._active = True
        self._notActiveCount = 0
        self._zapTimer = 0
        self._zapTime = 0.8
        self._start = True
        self._opposite = False

    def isActive(self):
        """returns if spawn is active or not"""
        return self._active

    def incNotActive(self):
        """increments the count of the spawn not being active"""
        self._notActiveCount += 1

    def notActive(self):
        """return the count of the spawn not being active"""
        return self._notActiveCount

    def handleBlobCollision(self):
        """handle the spawn colliding with a blob"""
        if self._opposite == False:
            self._opposite = True
        else:
            self._opposite = False

    def handleEnd(self):
        """handle a casual inactive moment"""
        newSpriteSize = Vector2(22,22)
        self._velocity = Vector2(0,0)
        self._imageName = "bubble_enemies.png"
        fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
        rect = pygame.Rect(newSpriteSize.x * 5, newSpriteSize.y * 2, newSpriteSize.x, newSpriteSize.y)
        self._image = pygame.Surface((rect.width,rect.height))
        self._image.blit(fullImage, (0,0), rect)
        self._image.set_colorkey(self._image.get_at((0,0)))
        self._active = False

    def handleDestroy(self):
        """handle a violent collision"""
        newSpriteSize = Vector2(22,22)
        self._velocity = Vector2(0,0)
        self._image = FRAMES.getFrame(self._imageName, (self._offsetX,1))
        self._active = False

    def update(self, worldInfo, ticks):
      """update the movement of the spawns"""
      newPosition = self._position
      if newPosition[0] < 0 or newPosition[0] > worldInfo[0]:
          self._active = False
      if self._position.x < 0:
          self.handleEnd()
      self._position.x += -self._velocity.x * ticks
