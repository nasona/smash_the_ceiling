"""
Abby Nason
smash! the ceiling
level_parser.py

Parses the level layout file and creates the level.
"""

import pygame
import os
import random
from modules.vector2D import Vector2
from characters.bra import Bra
from characters.pan import Pan
from characters.ring import Ring
from characters.devil import Devil
from characters.gaston import Gaston
from modules.drawable import Drawable
from characters.blob import Blob
from characters.elevator import Elevator
from characters.ceiling import Ceiling
from characters.boss import Boss
from characters.powerup import Floppy,Sign,Vote
from modules.soundManager import SoundManager

CHAR_SPRITE_SIZE = Vector2(32, 32)
SCALE = 2

class LevelParser:
    """creates a level"""
    def __init__(self, filename):
        """intializes a level"""
        self._filename = filename
        self._background = Drawable(self.getBackground(), Vector2(0,0), (0,0))
        self._ground = Drawable(self.getGround(), Vector2(0, 300), (0,0))
        self._blob = Blob(Vector2(0,300-CHAR_SPRITE_SIZE.y))
        self._decorations = []
        self._platforms = []
        self._traps = {"bra":[], "pan":[], "ring":[]}
        self._enemies = {"devil":[], "gaston": [], "boss": []}
        self._powerups = {"floppy": [], "sign": [], "vote": []}
        self._worldsize = (2400, 400)
        self._elevator = elevator = Elevator(Vector2(self._worldsize[0]-50,300), self._worldsize[1])
        if self._filename == "level3.txt":
            self._ceiling = Ceiling(Vector2(0, 0), final=False)
        elif self._filename == "level6.txt":
            self._ceiling = Ceiling(Vector2(0, 0), final=True)
        else:
            self._ceiling = None
        self._deathCycle = 0
        self._keydown = {1:False, 2:False, 3:False}
        self._otherblobs = []
        self._otherblobsCollideRect = None
        self._block = None
        self._spot = None
        self._activeBlobs = []
        self._downbar = None
        self._downbarSelections = []
        self._selectCount = 0
        self._samePlat = 0

    def getBackground(self):
        """returns the appropriate background image"""
        if self._filename == "level1.txt":
            backgroundImage = "background.png"
        elif self._filename == "level2.txt":
            backgroundImage = "background2.png"
        elif self._filename == "level3.txt" or self._filename == "level6.txt":
            backgroundImage = "background3b.png"
        elif self._filename == "level4.txt" or self._filename == "level5.txt":
            backgroundImage = "background4.png"
        return backgroundImage

    def getGround(self):
        """returns the appropriate ground image"""
        if self._filename == "level1.txt":
            groundImage = "ground2.png"
        elif self._filename == "level2.txt":
            groundImage = "ground3.png"
        elif self._filename == "level3.txt" or self._filename == "level6.txt":
            groundImage = "ground4b.png"
        elif self._filename == "level4.txt" or self._filename == "level5.txt":
            groundImage = "ground5.png"
        return groundImage

    def loadLevel(self):
        """controls the loading of the level"""
        file = open(os.path.join("resources", "levels", self._filename))
        fileContents = file.read()
        file.close()
        self.getWorldSize(fileContents)
        self._ground = Drawable(self.getGround(), Vector2(0, self._worldsize[1]-100), (0,0))
        if self._filename != "level6.txt":
            self._blob = Blob(Vector2(0,self._worldsize[1]-100-CHAR_SPRITE_SIZE.y), color=self._blob._color)
        self.plantFlowers()
        self.getPlatforms(fileContents)
        self.getOtherBlobs(fileContents)
        self.getActiveBlobs()
        self.getPowerUps(fileContents)
        self.getTraps(fileContents)
        self.getEnemies(fileContents)
        self.getWorldSize(fileContents)

    def reset(self):
        """resets a level"""
        self._decorations = []
        self._platforms = []
        self._traps = {"bra":[], "pan":[], "ring":[]}
        self._enemies = {"devil":[], "gaston": [], "boss": []}
        self._deathCycle = 0
        self._keydown = {1:False, 2:False, 3:False}
        self._powerups = {"floppy": [], "sign": [], "vote": []}
        self._otherblobs = []
        self._otherblobsCollideRect = None
        self._block = None
        self._spot = None
        self._activeBlobs = []

    def plantFlowers(self):
        """plants flowers randomly for decoration"""
        flowerSize = 16
        for xPos in range(0, 2400, 20):
            randomNumber = random.randint(10,13)
            self._decorations.append(Drawable("nuts_and_milk.png", Vector2(xPos, self._worldsize[1]-100-flowerSize), (randomNumber,8)))

    def getPlatforms(self, fileContents):
        """returns the appropriate platform tile image"""
        if self._filename == "level1.txt":
            platformImage = "platform.png"
        elif self._filename == "level2.txt":
            platformImage = "platform2.png"
        elif self._filename == "level3.txt" or self._filename == "level6.txt":
            platformImage = "platform3.png"
        elif self._filename == "level4.txt" or self._filename == "level5.txt":
            platformImage = "platform4.png"
        fileStuff = fileContents.split("\n")
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "platform":
                for i in range(int(info[3])):
                    self._platforms.append(Drawable(platformImage, Vector2(int(info[1]) + 50*i, int(info[2])), (0,0)))

    def getOtherBlobs(self, fileContents):
        """determines if this is a level that has other blobs in it that don't move"""
        fileStuff = fileContents.split("\n")
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "otherblobs":
                self._otherblobs.append(Blob(Vector2(int(info[2]),int(info[3])-CHAR_SPRITE_SIZE.y-50), color=info[1]))
        if len(self._otherblobs) != 0:
            self._otherblobsCollideRect = pygame.Rect(300,234,100,66)
            self._block = Drawable("block.png", Vector2(300,250), (0,0))
            self._spot = Drawable("ground.png", Vector2(250,300), (0,0))

    def getActiveBlobs(self):
        """determines if this is a level that the player can switch their controls between"""
        if self._filename == "level6.txt":
            self._activeBlobs.append(Blob(Vector2(25,100-CHAR_SPRITE_SIZE.y), color="pink"))
            self._activeBlobs.append(Blob(Vector2(25,self._worldsize[1]-100-CHAR_SPRITE_SIZE.y), color="blue"))
            self._activeBlobs.append(Blob(Vector2(200,self._worldsize[1]-100-CHAR_SPRITE_SIZE.y), color="green"))
            self._activeBlobs.append(Blob(Vector2(300,self._worldsize[1]-100-CHAR_SPRITE_SIZE.y), color="orange"))
            self._blob = self._activeBlobs[0]
            self._downbar = Drawable("downbar.png", Vector2(0,self._worldsize[1]-28), (0,0))
            for i in range(4):
                self._downbarSelections.append(Drawable("downbarselection.png", Vector2(i*28, self._worldsize[1]-28), (0,0)))

    def getTraps(self, fileContents):
        """parses the level layout file for the traps and saves them to a dictionary"""
        fileStuff = fileContents.split("\n")
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "trap":
                if info[1] == "bra":
                    self._traps[info[1]].append(Bra(Vector2(int(info[2]),int(info[3])-CHAR_SPRITE_SIZE.y)))
                elif info[1] == "ring":
                    self._traps[info[1]].append(Ring(Vector2(int(info[2]),int(info[3])-CHAR_SPRITE_SIZE.y)))
                elif info[1] == "pan":
                    self._traps[info[1]].append(Pan(Vector2(int(info[2]),int(info[3])-CHAR_SPRITE_SIZE.y)))

    def getEnemies(self, fileContents):
        """parses the level layout file for the enemies and saves them to a dictionary"""
        fileStuff = fileContents.split("\n")
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "enemy":
                if info[1] == "devil":
                    self._enemies[info[1]].append(Devil(Vector2(int(info[2]),int(info[3])-CHAR_SPRITE_SIZE.y), int(info[4])))
                elif info[1] == "gaston":
                    self._enemies[info[1]].append(Gaston(Vector2(int(info[2]),int(info[3])-CHAR_SPRITE_SIZE.y)))
                elif info[1] == "boss":
                    self._enemies[info[1]].append(Boss(Vector2(int(info[2]),int(info[3])-CHAR_SPRITE_SIZE.y-25)))

    def getPowerUps(self, fileContents):
       """parses the level layout file for the powerups and saves them to a dictionary"""
       fileStuff = fileContents.split("\n")
       for line in fileStuff:
           info = line.split(",")
           if info[0] == "powerup":
               if info[1] == "floppy":
                   self._powerups["floppy"].append(Floppy(Vector2(int(info[2]),int(info[3])-CHAR_SPRITE_SIZE.y)))
               elif info[1] == "sign":
                   self._powerups["sign"].append(Sign(Vector2(int(info[2]),int(info[3])-CHAR_SPRITE_SIZE.y)))
               elif info[1] == "vote":
                   self._powerups["vote"].append(Vote(Vector2(int(info[2]),int(info[3])-CHAR_SPRITE_SIZE.y)))


    def getWorldSize(self,fileContents):
        """parses the level layout file for the world size (vertical or horizontal)"""
        fileStuff = fileContents.split("\n")
        for line in fileStuff:
            info = line.split(",")
            if info[0] == "world size":
                self._worldsize = (int(info[1]), int(info[2]))

    def detectSelectedArea(self, mousePos):
        """figures out which blob the user has selected if there is a downbar"""
        for i in range(len(self._downbarSelections)):
            #print(mousePos)
            #print()
            #print(Drawable.WINDOW_OFFSET)
            if self._downbarSelections[i].getCollideRect().collidepoint(mousePos):
                #pink,blue,green,orange
                if i == 0:
                    #print("yes")
                    self._blob = self._activeBlobs[0]
                elif i == 1:
                    #print("yes")
                    self._blob = self._activeBlobs[1]
                elif i == 2:
                    #print("yes")
                    self._blob = self._activeBlobs[2]
                elif i == 3:
                    #print("yes")
                    self._blob = self._activeBlobs[3]

    def handleEvent(self, event):
        """handles key presses to determine if the user is using a cheat,
        selecting a blob, or controlling the blob"""
        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_1:
               self._keydown[1] = True
           if event.key == pygame.K_2:
               self._keydown[2] = True
           if event.key == pygame.K_3:
               self._keydown[3] = True
        elif event.type == pygame.KEYUP:
           if event.key == pygame.K_1:
               self._keydown[1] = False
           if event.key == pygame.K_2:
               self._keydown[2] = False
           if event.key == pygame.K_3:
               self._keydown[3] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #and self._selectCount == 0:
                mousePos = list([int(x/SCALE) for x in event.pos])
                #print(mousePos)
                adjustedPos = Drawable.adjustMousePos(mousePos)
                #print(adjustedPos)
                self.detectSelectedArea((adjustedPos.x, adjustedPos.y))
        self._blob.handleEvent(event)

    def draw(self, screen):
        """draws everything in the world"""
        self._background.draw(screen)
        self._ground.draw(screen)

        for decoration in self._decorations:
            decoration.draw(screen)

        for platform2 in self._platforms:
            platform2.draw(screen)

        if self._block != None:
            self._block.draw(screen)

        if self._spot != None:
            self._spot.draw(screen)

        for category2 in self._traps:
            for trap2 in self._traps[category2]:
                trap2.draw(screen)

        for bossie in self._enemies["boss"]:
            for spawn in bossie._spawns:
                #determines timing of the end of the animation
                if spawn.isActive():
                    spawn.draw(screen)
                elif spawn.notActive() > 15:
                    bossie._spawns.remove(spawn)
                else:
                    spawn.incNotActive()
                    spawn.draw(screen)

        for category10 in self._enemies:
            for enemy10 in self._enemies[category10]:
                enemy10.draw(screen)

        if self._filename != "level3.txt":
            for back in self._elevator._parts["back"]:
                back.draw(screen)

        if self._filename == "level3.txt" or self._filename == "level6.txt":
            self._ceiling.draw(screen)

        for typie in self._powerups:
            for powerup in self._powerups[typie]:
                #determines timing of the end of the animation
                if powerup.isActive():
                    powerup.draw(screen)
                elif powerup.notActive() > 5:
                    self._powerups[typie].remove(powerup)
                else:
                    powerup.incNotActive()
                    powerup.draw(screen)

        for b in self._otherblobs:
            b.draw(screen)

        for b2 in self._activeBlobs:
            b2.draw(screen)
        self._blob.draw(screen)

        for zap in self._blob._zaps:
            #determines timing of the end of the animation
            if zap.isActive():
                zap.draw(screen)
            elif zap.notActive() > 5:
                self._blob._zaps.remove(zap)
            else:
                zap.incNotActive()
                zap.draw(screen)

        if self._filename != "level3.txt" and self._filename != "level6.txt":
            for part in self._elevator._parts:
                if part != "back":
                    for section in self._elevator._parts[part]:
                        section.draw(screen)

        for ringy in self._traps["ring"]:
            for zappy in ringy._zaps:
                #determines timing of the end of the animation
                if zappy.isActive():
                    zappy.draw(screen)
                elif zappy.notActive() > 5:
                    ringy._zaps.remove(zappy)
                else:
                    zappy.incNotActive()
                    zappy.draw(screen)

        for gas in self._enemies["gaston"]:
            for arrow15 in gas._arrows:
                #determines timing of the end of the animation
                if arrow15.isActive():
                    arrow15.draw(screen)
                elif arrow15.notActive() > 5:
                    gas._arrows.remove(arrow15)
                else:
                    arrow15.incNotActive()
                    arrow15.draw(screen)

        if self._downbar != None:
            self._downbar.draw(screen)

    def detectCollision(self):
         """detects collisions between objects in the level"""
         #remove bra if it has been ran into by blob but keep the pan
         for category3 in self._traps:
            for trap3 in self._traps[category3]:
                if trap3.ranInto():
                    if category3 == "bra":
                        self._traps[category3].remove(trap3)
                    elif category3 == "pan":
                        trap3.resetRanInto()

         #variable to determine if blob already collided with the ground
         clipRect = self._blob.getCollideRect().clip(self._ground.getCollideRect())

         if clipRect.width > 0:
            if self._samePlat != self._blob._position.y:
                self._samePlat = self._blob._position.y
                SoundManager.getInstance().playSound("plop.ogg")
            self._blob.manageState("collideGround")

         i = True
         blobPos = self._blob.getCollideRect()
         totalClipWidth = 0

         #determine blob collision with the ceiling on level 3
         if self._filename == "level3.txt":
             if self._blob._position.y <= 25:
                 self._blob.manageState("fall")
                 if self._blob._velocity.y < 0:
                     self._blob._velocity.y = -self._blob._velocity.y
                     if self._blob._position.x <= 200:
                         self._ceiling.incHP("left")
                     elif self._blob._position.x > 200:
                         self._ceiling.incHP("right")
                 self._ceiling.updateVisual()

         #determine blob collision with ceiling on level 6
         if self._filename == "level6.txt":
             if self._blob._position.y <= 25:
                 self._blob.manageState("fall")
                 if self._blob._velocity.y < 0:
                     self._blob._velocity.y = -self._blob._velocity.y
                     if self._blob._position.x <= 200 and self._activeBlobs[0]._position.y < 150 and self._activeBlobs[1]._position.y < 150 and self._activeBlobs[1]._position.y < 150 and self._activeBlobs[1]._position.y < 150:
                         self._ceiling.incHP("left", self._blob._color)
                     elif self._blob._position.x > 200 and self._activeBlobs[0]._position.y < 150 and self._activeBlobs[1]._position.y < 150 and self._activeBlobs[1]._position.y < 150 and self._activeBlobs[1]._position.y < 150:
                         self._ceiling.incHP("right", self._blob._color)
                 self._ceiling.updateVisual()

         #determine if the blob has collided with platforms
         for platform in self._platforms:
             platPos = platform.getCollideRect()
             clipRect2 = blobPos.clip(platPos)
             totalClipWidth += clipRect2.width
             if clipRect2.height >= 3 and blobPos[1]+20 >= platPos[1]:
                 if blobPos[0] < platPos[0] and self._blob._velocity.x >= 0:
                     if self._blob._velocity.x == 0:
                         self._blob._velocity.x = -100
                     else:
                         self._blob._velocity.x = -self._blob._velocity.x
                 elif blobPos[0] + blobPos[2] > platPos[0] + platPos[2] and self._blob._velocity.x <= 0:
                     if self._blob._velocity.x == 0:
                         self._blob._velocity.x = 100
                     else:
                         self._blob._velocity.x = -self._blob._velocity.x
                 if self._blob._velocity.y <= 0:
                     self._blob._velocity.y = -self._blob._velocity.y
                 self._blob.manageState("fall")
             elif (clipRect2.width >= 5 or (clipRect2.width > 0 and totalClipWidth == 32)) and blobPos[1] + blobPos[3] <= platPos[1] + platPos[3]:
                 #make sure this is the first time the blob has collided with the platofrm before playing the sound effect
                 if self._samePlat != self._blob._position.y:
                     self._samePlat = self._blob._position.y
                     SoundManager.getInstance().playSound("plop.ogg")
                 self._blob.manageState("collidePlatform")
                 i = False
             elif clipRect2.width < 5 and self._blob._FSM == "platformed" and i:
                 self._blob.manageState("fall")
                 self._blob.updateVisual()

         #keep the blobs that are not selected in level 6 in their grounded/platformed image
         if self._filename == "level6.txt":
            for otraBlob in self._activeBlobs:
                if otraBlob != self._blob:
                    otraBlob.updateVisual(inactive=True)
                    if otraBlob._position.y >= self._worldsize[1] - 100:
                        otraBlob.manageState("collideGround")
                    else:
                        otraBlob.manageState("collidePlatform")

         #determine if blob has collided with a trap
         for category in self._traps:
             for trap in self._traps[category]:
                 if self._blob.getCollideRect().colliderect(trap.getCollideRect()):
                     trap.handleCollision()
                     if category == "bra":
                         self._blob._velocity.x = -self._blob._velocity.x
                         if not self._blob._forcefield:
                             self._blob.die()
                     elif category == "pan":
                         self._blob._velocity.x = -self._blob._velocity.x * 0.5
                         self._blob._velocity.y = -self._blob._velocity.y
                         if not self._blob._forcefield:
                             self._blob.die()
                     elif category == "ring":
                         if blobPos[0] + blobPos[2] > trap.getCollideRect()[0] + trap.getCollideRect()[2]:
                             self._blob._velocity.x = 100
                         else:
                             self._blob._velocity.x = -100
                         self._blob._velocity.y = -self._blob._velocity.y

         #determine if a blob has collided with powerup that makes forcefield
         for powerupT1 in self._powerups["floppy"]:
             if self._blob.getCollideRect().colliderect(powerupT1.getCollideRect()):
                 powerupT1.handleEnd()
                 SoundManager.getInstance().playSound("powerup.ogg")
                 self._blob.activateForcefield()

         #determine if a blob has collided with powerup that increases jump time
         for powerupT2 in self._powerups["sign"]:
             if self._blob.getCollideRect().colliderect(powerupT2.getCollideRect()):
                 powerupT2.handleEnd()
                 SoundManager.getInstance().playSound("powerup.ogg")
                 self._blob.increaseJumpTime()

         #determine if a blob has collided with powerup that teleports them forward
         for powerupT3 in self._powerups["vote"]:
             if self._blob.getCollideRect().colliderect(powerupT3.getCollideRect()):
                 powerupT3.handleEnd()
                 SoundManager.getInstance().playSound("powerup.ogg")
                 self._blob.moveForward(self._filename)

         #determine if a heart the blob shoots has collided with traps
         for category4 in self._traps:
             for trap4 in self._traps[category4]:
                 for zap4 in self._blob._zaps:
                     if zap4.getCollideRect().colliderect(trap4.getCollideRect()):
                         if category4 == "bra":
                             trap4.handleCollision()
                             zap4.handleDestroy()
                             SoundManager.getInstance().playSound("explosion.ogg")
                         if category4 == "pan":
                             self._traps[category4].remove(trap4)
                             zap4.handleDestroy()
                             SoundManager.getInstance().playSound("explosion.ogg")
                         elif category4 == "ring":
                              zap4.handleEnd()

         #determine if a heart the blob shoots has collided with enemies
         for category17 in self._enemies:
             for enemy17 in self._enemies[category17]:
                 for zap17 in self._blob._zaps:
                     if zap17.getCollideRect().colliderect(enemy17.getCollideRect()):
                         enemy17.handleCollision()
                         zap17.handleDestroy()
                         SoundManager.getInstance().playSound("explosion.ogg")
                         if enemy17.isDead() and enemy17 in self._enemies[category17]:
                             self._enemies[category17].remove(enemy17)

         #determine if the blob has collided with enemies
         for category21 in self._enemies:
             for enemy21 in self._enemies[category21]:
                 if self._blob.getCollideRect().colliderect(enemy21.getCollideRect()):
                     self._blob._velocity.x = -self._blob._velocity.x
                     if category21 == "devil" or category21 == "boss":
                         if not self._blob._forcefield:
                             self._blob.die()

         #determine if a heart the blob shoots has collided with what the ring shoots
         for ring7 in self._traps["ring"]:
             for ringZap in ring7._zaps:
                 for blobZap in self._blob._zaps:
                     if ringZap.getCollideRect().colliderect(blobZap.getCollideRect()):
                         SoundManager.getInstance().playSound("explosion.ogg")
                         ringZap.handleDestroy()
                         SoundManager.getInstance().playSound("explosion.ogg")
                         blobZap.handleDestroy()

         #determine if a heart the blob shoots has collided with gaston's arrows
         for gaston50 in self._enemies["gaston"]:
             for arrow50 in gaston50._arrows:
                 for blobZap50 in self._blob._zaps:
                     if arrow50.getCollideRect().colliderect(blobZap50.getCollideRect()):
                         arrow50.handleDestroy()
                         SoundManager.getInstance().playSound("explosion.ogg")
                         blobZap50.handleDestroy()
                         SoundManager.getInstance().playSound("explosion.ogg")

         #determine if a heart the blob shoots has collided with traps
         for boss2 in self._enemies["boss"]:
             for spawn2 in boss2._spawns:
                 for blobZap200 in self._blob._zaps:
                     if spawn2.getCollideRect().colliderect(blobZap200.getCollideRect()):
                         SoundManager.getInstance().playSound("explosion.ogg")
                         spawn2.handleDestroy()
                         SoundManager.getInstance().playSound("explosion.ogg")
                         blobZap200.handleDestroy()
                         self._blob.die()

         #determine if a spawn has collided with the blob
         for boss3 in self._enemies["boss"]:
             for spawn3 in boss3._spawns:
                 if self._blob.getCollideRect().colliderect(spawn3.getCollideRect()):
                      self._blob._velocity.x = -self._blob._velocity.x
                      spawn3._velocity.x = -spawn3._velocity.x
                      spawn3.handleBlobCollision()

         #determine if currently selected blob has collided with another active blob
         for b4 in self._activeBlobs:
             if b4 != self._blob:
                 if self._blob.getCollideRect().colliderect(b4.getCollideRect()):
                     self._blob._velocity.x = -self._blob._velocity.x
                     self._blob._velocity.y = -self._blob._velocity.y

         #determine if currently selected blob has collided with another inactive blob
         if self._otherblobsCollideRect != None:
             if self._blob.getCollideRect().colliderect(self._otherblobsCollideRect):
                 self._blob._velocity.x = -150
                 self._blob._velocity.y = -self._blob._velocity.y

         #determine if a boss has collided with its spawns
         for boss4 in self._enemies["boss"]:
             for spawn4 in boss4._spawns:
                 if boss4.getCollideRect().colliderect(spawn4.getCollideRect()) and spawn4._opposite == True:
                     spawn4._velocity.x = 0
                     spawn4.handleEnd()
                     #spawn4.handleBlobCollision()

         #determine if a spawn has collided with other spawns
         for boss5 in self._enemies["boss"]:
             for spawn5a in boss5._spawns:
                 for spawn5b in boss5._spawns:
                     if spawn5a != spawn5b:
                         if spawn5a.getCollideRect().colliderect(spawn5b.getCollideRect()):
                             if spawn5a._opposite == False and spawn5b._opposite == True:
                                 #if spawn5b._velocity.x == -spawn5a._velocity.x or spawn5a._velocity.x != 0:
                                 spawn5b._velocity.x = spawn5a._velocity.x
                                 spawn5b.handleBlobCollision()
                             elif spawn5b._opposite == False and spawn5a._opposite == True:
                                 #if spawn5b._velocity.x == -spawn5a._velocity.x  or spawn5b._velocity.x != 0:
                                 spawn5a._velocity.x = spawn5b._velocity.x
                                 spawn5a.handleBlobCollision()

         #determine if a spawn has collided with a trap
         for category57 in self._traps:
             for trap57 in self._traps[category57]:
                 for boss57 in self._enemies["boss"]:
                     for spawn57 in boss57._spawns:
                         if spawn57.getCollideRect().colliderect(trap57.getCollideRect()):
                             spawn57.handleEnd()


         #handle collision with harmful things shot at blob if it has a forcefield
         if self._blob._forcefield:
             for ring40 in self._traps["ring"]:
                 for ringZap40 in ring40._zaps:
                     if ringZap40.getCollideRect().colliderect(self._blob.getCollideRect()):
                         SoundManager.getInstance().playSound("explosion.ogg")
                         ringZap40.handleDestroy()

             for gaston82 in self._enemies["gaston"]:
                 for arrow82 in gaston82._arrows:
                     if arrow82.getCollideRect().colliderect(self._blob.getCollideRect()):
                         arrow82.handleDestroy()

         #handle collision with ring zaps shot at blob without a forcefield
         for ring20 in self._traps["ring"]:
             for zap20 in ring20._zaps:
                 if zap20.getCollideRect().colliderect(self._blob.getCollideRect()):
                     SoundManager.getInstance().playSound("explosion.ogg")
                     zap20.handleDestroy()
                     if not self._blob._forcefield:
                         self._blob.die()

         #handle collision with gaston's arrows and blob without a forcefield
         for gaston64 in self._enemies["gaston"]:
             for arrow64 in gaston64._arrows:
                 if arrow64.getCollideRect().colliderect(self._blob.getCollideRect()):
                     SoundManager.getInstance().playSound("explosion.ogg")
                     arrow64.handleDestroy()
                     if not self._blob._forcefield:
                         self._blob.die()

         #handle collision with blob zaps and elevator
         for door in self._elevator._parts["doors"]:
             for zap102 in self._blob._zaps:
                 if zap102.getCollideRect().colliderect(door.getCollideRect()):
                     zap102.handleEnd()

         #handle collision with blob zaps and powerups
         for typie811 in self._powerups:
             for powerup811 in self._powerups[typie811]:
                 for zap811 in self._blob._zaps:
                     if zap811.getCollideRect().colliderect(powerup811.getCollideRect()):
                         zap811.handleEnd()

         #handle collision with blob zaps and ring zaps with a platform
         for platform3 in self._platforms:
             for zap5 in self._blob._zaps:
                 if zap5.getCollideRect().colliderect(platform3.getCollideRect()):
                     zap5.handleEnd()
             for ring15 in self._traps["ring"]:
                 for zap15 in ring15._zaps:
                     if zap15.getCollideRect().colliderect(platform3.getCollideRect()):
                         zap15.handleEnd()

    def update(self, WORLD_SIZE, SCREEN_SIZE, ticks):
        """updates all of the objects in the current level in the world"""
        #determine if cheat is being used: take blob to end of level
        if self._keydown[1] == True and self._keydown[2] == True and self._keydown[3] == True:
            if self._filename != "level3.txt" and self._filename != "level6.txt":
                self._blob.update(WORLD_SIZE, ticks, cheat=True, horizontal=True)
            else:
                self._blob.update(WORLD_SIZE, ticks, cheat=True, horizontal=False)
        else:
            #otherwise update blob normally
            self._blob.update(WORLD_SIZE, ticks)
        #update pan animation
        for pan in self._traps["pan"]:
            pan.update(ticks)
        #update blob zaps movement
        for zap2 in self._blob._zaps:
            zap2.update(WORLD_SIZE, ticks)
        #update devil animation and movement
        for devil in self._enemies["devil"]:
            devil.update(WORLD_SIZE, ticks)
        #update gaston animation and movement of his arrows
        for gaston in self._enemies["gaston"]:
            gaston.update(WORLD_SIZE, ticks)
        #update ring zap movement
        for ring in self._traps["ring"]:
            ring.update(WORLD_SIZE, ticks)
        #update boss animation and spawn movements
        for boss in self._enemies["boss"]:
            boss.update(WORLD_SIZE, ticks)

        #update ceiling falling once ceiling is smashed in final level
        if self._filename == "level6.txt" and self._ceiling.readyForNextLevel():
            SoundManager.getInstance().playSound("big_smash.ogg")
            self._ceiling.update(ticks)

        #if blob is dead, reset the level
        if self._blob.isDead():
            if self._deathCycle > 30:
                self.reset()
                self.loadLevel()
                # initialize the blob on top of the ground
                self._blob = Blob(Vector2(0,WORLD_SIZE[1]-100-CHAR_SPRITE_SIZE.y), self._blob._color)
                self._deathCycle = 0
            else:
                self._deathCycle += 1



        # getting the offset of the of the current blob (our tracking object)
        Drawable.updateOffset(self._blob, SCREEN_SIZE, WORLD_SIZE)

        #update the position of the downbar on the final level
        if self._downbar != None:
            self._downbar._position = Vector2(Drawable.WINDOW_OFFSET.x, Drawable.WINDOW_OFFSET.y + SCREEN_SIZE[1]-28)
            for i in range(4):
                self._downbarSelections[i]._position = Vector2(i*28 + Drawable.WINDOW_OFFSET.x, Drawable.WINDOW_OFFSET.y + SCREEN_SIZE[1]-28)
                #print(self._downbarSelections[i]._position)




def main():
    parser = selfParser("level1.txt")
    parser.loadLevel()

if __name__ == "__main__":
   main()
