"""
Abby Nason
Project 1
main.py

Displays a star which moves based on arrow key input. When the mouse is clicked, an orb is
introduced to the world at that position and moves in a random direction. When the star and
an orb collide, the orb "dies" and is removed from the game. Both star and orb objects rebound
against the edge of the world The window follows the star around the world.
"""



import pygame
import os
from modules.vector2D import Vector2
import random
from characters.orb import Orb
from characters.blob import Blob
from characters.bra import Bra
from characters.pan import Pan
from characters.ring import Ring
from modules.drawable import Drawable
from modules.level_parser import LevelParser
#from modules.gameManager import GameManager

# screen size is the amount we show the player
# world size is the size of the interactable world
SCREEN_SIZE = (400, 400)
WORLD_SIZE = (2400, 400)
CHAR_SPRITE_SIZE = Vector2(32, 32)

def main():

   # initialize the pygame module
   pygame.init()

   # load and set the logo
   pygame.display.set_caption("Smash! the Ceiling")

   # creating the screen
   screen = pygame.display.set_mode(SCREEN_SIZE)

   platforms = []
   traps = []

   background = Drawable("background.png", Vector2(0,0), (0,0))
   ground = Drawable("ground2.png", Vector2(0, 300), (0,0))

   level = LevelParser("level2.txt")
   level.loadLevel()
   print(level._traps["ring"][0].getCollideRect())
   #platform1a = Drawable("platform.png", Vector2(150, 200), (0,0))
   #platform1b = Drawable("platform.png", Vector2(200, 200), (0,0))
   #platform2a = Drawable("platform.png", Vector2(400, 250), (0,0))
   #platform3a = Drawable("platform.png", Vector2(475, 150), (0,0))
   #platform3b = Drawable("platform.png", Vector2(525, 150), (0,0))
   #platform3c = Drawable("platform.png", Vector2(575, 150), (0,0))
   #platform4a = Drawable("platform.png", Vector2(600, 150), (0,0))
   #platform4b = Drawable("platform.png", Vector2(650, 150), (0,0))
   #platform4c = Drawable("platform.png", Vector2(700, 150), (0,0))
   #platform5a = Drawable("platform.png", Vector2(625, 275), (0,0))
   #platform5b = Drawable("platform.png", Vector2(675, 275), (0,0))
   #platform6a = Drawable("platform.png", Vector2(750, 250), (0,0))
   #platform7a = Drawable("platform.png", Vector2(1000, 200), (0,0))
   #platform7b = Drawable("platform.png", Vector2(1050, 200), (0,0))
   #platform8a = Drawable("platform.png", Vector2(1125, 100), (0,0))
   #platform8b = Drawable("platform.png", Vector2(1175, 100), (0,0))
   #platform9a = Drawable("platform.png", Vector2(1500, 200), (0,0))
   #platform9b = Drawable("platform.png", Vector2(1550, 200), (0,0))
   #platform9c = Drawable("platform.png", Vector2(1600, 200), (0,0))
   #platforms = [platform1a, platform1b, platform2a, platform3a, platform3b, platform3c, platform4a, platform4b, platform4c, platform5a, platform5b, platform6a, platform7a, platform7b, platform8a, platform8b, platform9a, platform9b, platform9c]

   #bra = Bra(Vector2(200,300-CHAR_SPRITE_SIZE.y))
   #traps.append(bra)
   #pan = Pan(Vector2(400,300-CHAR_SPRITE_SIZE.y))
   #traps.append(pan)
   #ring = Ring(Vector2(200,200-CHAR_SPRITE_SIZE.y))
   #traps.append(ring)

   # initialize the blob on top of the ground
   blob = Blob(Vector2(0,300-CHAR_SPRITE_SIZE.y))

   # initialize the orb list
   #orbs = []

   # set the offset of the window into the world
   offset = Vector2(0,0)

   # initialize the game clock
   gameClock = pygame.time.Clock()

   # define a variable to control the main loop
   RUNNING = True

   # main loop
   while RUNNING:

      gameClock.tick()

      # draw everything based on the offset
      #screen.blit(background, (-offset[0], -offset[1]))
      background.draw(screen)
      ground.draw(screen)
      for decoration in level._decorations:
          decoration.draw(screen)
      for platform2 in level._platforms:
          platform2.draw(screen)
      for category2 in level._traps:
          for trap2 in level._traps[category2]:
              trap2.draw(screen)
      blob.draw(screen)
      for zap in blob._zaps:
          if zap.isActive():
              zap.draw(screen)
          else:
              blob._zaps.remove(zap)
      #for orb in orbs:
        #orb.draw(screen)

      for category3 in level._traps:
          for trap3 in level._traps[category3]:
              if trap3.ranInto():
                  if category3 == "bra":
                      level._traps[category3].remove(trap3)
                  elif category3 == "pan":
                      trap3.resetRanInto()
      # flip display to the monitor
      pygame.display.flip()

      clipRect = blob.getCollideRect().clip(ground.getCollideRect())

      if clipRect.width > 0:
         blob.manageState("collideGround")

      #variable to determine if already collided with a platform
      i = True
      blobPos = blob.getCollideRect()
      totalClipWidth = 0
      for platform in level._platforms:
          platPos = platform.getCollideRect()
          clipRect2 = blobPos.clip(platPos)
          totalClipWidth += clipRect2.width
          if clipRect2.height >= 3 and blobPos[1]+20 >= platPos[1]:
              if blobPos[0] < platPos[0] and blob._velocity.x >= 0:
                  if blob._velocity.x == 0:
                      blob._velocity.x = -100
                  else:
                      blob._velocity.x = -blob._velocity.x
              elif blobPos[0] + blobPos[2] > platPos[0] + platPos[2] and blob._velocity.x <= 0:
                  if blob._velocity.x == 0:
                      blob._velocity.x = 100
                  else:
                      blob._velocity.x = -blob._velocity.x
              if blob._velocity.y <= 0:
                  blob._velocity.y = -blob._velocity.y
              blob.manageState("fall")
          elif (clipRect2.width >= 5 or (clipRect2.width > 0 and totalClipWidth == 32)) and blobPos[1] + blobPos[3] <= platPos[1] + platPos[3]:
              blob.manageState("collidePlatform")
              i = False
          elif clipRect2.width < 5 and blob._FSM == "platformed" and i:
              blob.manageState("fall")
              blob.updateVisual()

      for category in level._traps:
          for trap in level._traps[category]:
              if blob.getCollideRect().colliderect(trap.getCollideRect()):
                  trap.handleCollision()
                  if category == "bra":
                      blob._velocity.x = -blob._velocity.x
                  elif category == "pan":
                      blob._velocity.x = -blob._velocity.x * 0.5
                      blob._velocity.y = -blob._velocity.y
                  elif category == "ring":
                      if blobPos[0] + blobPos[2] > trap.getCollideRect()[0] + trap.getCollideRect()[2]:
                          blob._velocity.x = 100
                      else:
                          blob._velocity.x = -100
                      blob._velocity.y = -blob._velocity.y

      for category4 in level._traps:
          for trap4 in level._traps[category4]:
              for zap4 in blob._zaps:
                  print(zap4.getCollideRect())
                  print(trap4.getCollideRect())
                  if zap4.getCollideRect().colliderect(trap4.getCollideRect()):
                      level._traps[category4].remove(trap4)


      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or ESCAPE is pressed
         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False to exit the main loop
            RUNNING = False
         # handle arrow key up and down events
         else:
             blob.handleEvent(event)

      # update everything
      ticks = gameClock.get_time() / 1000
      blob.update(WORLD_SIZE, ticks)
      for pan in level._traps["pan"]:
          pan.update(ticks)
      for zap2 in blob._zaps:
          zap2.update(WORLD_SIZE, ticks)
      #for orb in orbs:
        #orb.update(WORLD_SIZE, ticks)

      # Detect collision
      #for orb in orbs:
        #  if orb.getCollideRect().colliderect(star.getCollideRect()):
        #      orb.kill()

      # remove the dead orbs before the next iteration
      #for orb in orbs:
        #  if orb.isDead():
        #      orbs.remove(orb)

      # getting the offset of the of the star (our tracking object)
      Drawable.updateOffset(blob, SCREEN_SIZE, WORLD_SIZE)

if __name__ == "__main__":
   main()
