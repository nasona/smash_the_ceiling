"""
Abby Nason
Project 2
star.py

Defines the Star class, which inherits from the Drawable class.
"""

import pygame
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.mobile import Mobile
import os

SPRITE_SIZE = Vector2(32, 32)
MAX_VELOCITY = 15
ACCELERATION = 5.0

class Blob(Mobile):

    def __init__(self, position):
        """initializes to orb class by inheriting from the Drawable class and
        with instance variables: _velocity, _maxVelocity, _acceleration, and _movement"""
        super().__init__("blobs.png", position, pygame.Rect(0, 0, SPRITE_SIZE.x, SPRITE_SIZE.y)) #, pygame.Rect(0, 0, SPRITE_SIZE.x, SPRITE_SIZE.y), True)
        #a vector2 of its velocity
        self._velocity = Vector2(0,0)
        self._maxVelocity = MAX_VELOCITY
        self._acceleration = ACCELERATION
        self._movement = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
        self._jumpTimer = 0
        self._jumpTime = 0.75
        self._vSpeed = 100
        self._jSpeed = 100

    # Public access to tell jumper to try to take some action, typically for collision
    def manageState(self, action):
      self._FSM.manageState(action)

    def handleEvent(self, event):
      # attempt to manage state based on keypresses
      if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_LEFT:
            self._movement[pygame.K_LEFT] = True
            self._FSM.manageState("left")
         elif event.key == pygame.K_RIGHT:
            self._movement[pygame.K_RIGHT] = True
            self._FSM.manageState("right")
            # Check for jumping keypress
         elif event.key == pygame.K_UP:
            self._movement[pygame.K_UP] = True
            self._FSM.manageState("jump")
            self.updateVisual()
         elif event.key == pygame.K_DOWN:
            self._movement[pygame.K_DOWN] = True
            self._FSM.manageState("duck")
            self.updateVisual()
      elif event.type == pygame.KEYUP:
         if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
            if event.key == pygame.K_LEFT:
                self._movement[pygame.K_LEFT] = False
            if event.key == pygame.K_RIGHT:
                self._movement[pygame.K_RIGHT] = False
            self._FSM.manageState("stopMoving")
        # check for release of jumping keypress
         elif event.key == pygame.K_UP:
            self._movement[pygame.K_UP] = False
            self._FSM.manageState("fall")
         elif event.key == pygame.K_DOWN:
            self._movement[pygame.K_DOWN] = False
            if self._position.y + 32 >= 300:
                self._FSM.manageState("collideGround")
            else:
                self._FSM.manageState("collidePlatform")
            self.updateVisual()

    def update(self, worldInfo, ticks):
      newPosition = self._position
      if newPosition[0] < 0 or newPosition[0] > worldInfo[0]:
          self._velocity.x = -self._velocity.x
      super().update(ticks)
      # decrease the jump timer by ticks
      if self._FSM == "jumping":
          self._jumpTimer += ticks

          if self._jumpTimer > self._jumpTime:
              self._FSM.manageState("fall")
      elif self._FSM == "grounded" or self._FSM == "platformed":
          self._jumpTimer = 0
          self.updateVisual()

    def updateVisual(self):
        fullImage = pygame.image.load(os.path.join("images", self._imageName)).convert()
        if self._FSM.isDucking():
            y = 1
        if self._FSM.isJumping() or self._FSM.isFalling():
            y = 2
        else:
            y = 0
        rect = pygame.Rect(0, SPRITE_SIZE.y * y, SPRITE_SIZE.x, SPRITE_SIZE.y)
        self._image = pygame.Surface((rect.width,rect.height))
        self._image.blit(fullImage, (0,0), rect)
        self._image.set_colorkey(self._image.get_at((0,0)))

    def move(self, event):
        """sets the values in the _movement dictionary based on which arrow keys
        are up (False) and which keys are down (True)"""
        #keydown event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self._movement[pygame.K_DOWN] = True
            elif event.key == pygame.K_UP:
                self._movement[pygame.K_UP] = True
            elif event.key == pygame.K_LEFT:
                self._movement[pygame.K_LEFT] = True
            elif event.key == pygame.K_RIGHT:
                self._movement[pygame.K_RIGHT] = True
        #keyup event
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self._movement[pygame.K_DOWN] = False
            elif event.key == pygame.K_UP:
                self._movement[pygame.K_UP] = False
            elif event.key == pygame.K_LEFT:
                self._movement[pygame.K_LEFT] = False
            elif event.key == pygame.K_RIGHT:
                self._movement[pygame.K_RIGHT] = False
"""
    def update(self, worldInfo, ticks):
        #updates the star's position based on its current velocity
        #handle velocity according to the keys that are pressed
        if self._movement[pygame.K_DOWN]:
            self._velocity.y += self._acceleration
        if self._movement[pygame.K_UP]:
            self._velocity.y += -self._acceleration
        if self._movement[pygame.K_LEFT]:
            self._velocity.x += -self._acceleration
        if self._movement[pygame.K_RIGHT]:
            self._velocity.x += self._acceleration

        #scale the velocity if the star's magnitude exceeds max velocity
        if self._velocity.magnitude() > self._maxVelocity:
            self._velocity.scale(self._maxVelocity)

        #handle if the star is going to exceed the world bounds
        newPosition = self._position + self._velocity * ticks
        if newPosition[0] < 0 or newPosition[0] > worldInfo[0]:
            self._velocity.x = -self._velocity.x
        if newPosition[1] < 0 or newPosition[1] > worldInfo[1]:
            self._velocity.y = -self._velocity.y
        newPosition = self._position + self._velocity * ticks
        self._position = newPosition
        """
