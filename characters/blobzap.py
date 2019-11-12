import pygame
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.mobile import Mobile
import os

SPRITE_SIZE = Vector2(16, 16)
MAX_VELOCITY = 250
ACCELERATION = 5.0
ZAP_RANGE = 50

class BlobZap(Mobile):

    def __init__(self, position):
        """initializes to orb class by inheriting from the Drawable class and
        with instance variables: _velocity, _maxVelocity, _acceleration, and _movement"""
        #super().__init__("blobs.png", position, pygame.Rect(0, 0, SPRITE_SIZE.x, SPRITE_SIZE.y)) #, pygame.Rect(0, 0, SPRITE_SIZE.x, SPRITE_SIZE.y), True)
        super().__init__("nuts_and_milk.png", position, (11,1))
        #a vector2 of its velocity
        self._originalPosition = position
        self._velocity = Vector2(MAX_VELOCITY,0)
        #self._maxVelocity = MAX_VELOCITY
        #self._acceleration = ACCELERATION
        self._active = True
        self._notActiveCount = 0
        self._zapTimer = 0
        self._zapTime = 0.75
        self._movement = {pygame.K_LEFT: False, pygame.K_RIGHT: True}
        self._start = True

    def isActive(self):
        return self._active

    def incNotActive(self):
        self._notActiveCount += 1

    def notActive(self):
        return self._notActiveCount

    def handleEnd(self):
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
        newSpriteSize = Vector2(22,22)
        self._velocity = Vector2(0,0)
        self._imageName = "bubble_enemies.png"
        fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
        rect = pygame.Rect(newSpriteSize.x * 4, newSpriteSize.y * 2, newSpriteSize.x, newSpriteSize.y)
        self._image = pygame.Surface((rect.width,rect.height))
        self._image.blit(fullImage, (0,0), rect)
        self._image.set_colorkey(self._image.get_at((0,0)))
        self._active = False

    def handleEvent(self, event):
      # attempt to manage state based on keypresses
      if self._start:
          self._start = False
          if event:
            self._movement[pygame.K_LEFT] = True
            self._movement[pygame.K_RIGHT] = False
          else:
            self._movement[pygame.K_LEFT] = False
            self._movement[pygame.K_RIGHT] = True

    def update(self, worldInfo, ticks):
      newPosition = self._position
      if newPosition[0] < 0 or newPosition[0] > worldInfo[0]:
          self._active = False
      self._zapTimer += ticks
      if self._zapTimer > self._zapTime:
          #self._active = False
          self.handleEnd()
      if self._movement[pygame.K_LEFT]:
          self._position.x += -self._velocity.x * ticks
      else:
          self._position.x += self._velocity.x * ticks
      #super().update(ticks)