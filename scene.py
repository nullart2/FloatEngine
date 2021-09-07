#Uses Python with SDL2
#C++/C# is Not Yet Supported

import pygame
from pygame.surfarray import array_alpha
import utils
import globals
import engine

class Scene():
    def __init__(self):
        pass    
    def onEnter(self):
        pass
    def onExit(self):
        pass
    def update(self, sm):
        pass
    def input(self, sm):
        pass   
    def draw(self, sm, screen):
        pass

class MainMenuScene(Scene):
    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            sm.push(FadeTransitionScene(self, LevelSelectScene()))
        if keys[pygame.K_z]:
            sm.pop()
    def draw(self, sm, screen):
        #draw menu
        screen.fill(globals.Blue)
        utils.drawLargeText(screen, 'Float Engine Demo', 30, 30) 
        utils.drawText(screen, 'Press ENTER to Start', 30, 200)
        utils.drawSmallText(screen, 'Version 0.0.2', 600, 450)

class LevelSelectScene(Scene): #may remove in future update
    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            sm.push(FadeTransitionScene(self, GameScene()))
        if keys[pygame.K_2]:
            sm.push(FadeTransitionScene(self, GameScene()))
        if keys[pygame.K_ESCAPE]:
            sm.pop()
            sm.push(FadeTransitionScene(self, MainMenuScene()))
    def draw(self, sm, screen):
        #draw level menu
        screen.fill(globals.Blue)
        utils.drawLargeText(screen, 'Level Select', 30, 30) 
        utils.drawText(screen, 'Level 1, Press 1', 30, 200)
        utils.drawText(screen, 'Level 2, Press 2', 30, 300)
        utils.drawSmallText(screen, 'Version 0.0.2', 600, 450)

class GameScene(Scene):
    def __init__(self):
        self.cameraSystem = engine.CameraSystem()
    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sm.pop()
            sm.push(FadeTransitionScene(self, LevelSelectScene()))
    def update(self, sm):
        pass
    def draw(self, sm, screen):
        self.cameraSystem.update(screen)

class Transition(Scene):
    def __init__(self, fromScene, toScene):
        self.currentPercentage = 0
        self.fromScene = fromScene
        self.toScene = toScene
    def update(self, sm):
        self.currentPercentage += 1
        if self.currentPercentage >= 100:
            sm.pop()
            sm.push(self.toScene)

class FadeTransitionScene(Transition):
    def draw(self, sm, screen):
        if self.currentPercentage < 50:
            self.fromScene.draw(sm, screen)
        else:
            self.toScene.draw(sm, screen)
            #fade effect logic
            overlay = pygame.Surface((700,500))
            alpha = int(abs(255 - (255/50)*self.currentPercentage))
            overlay.set_alpha(255 - alpha)
            #effect display
            overlay.fill(globals.Black)
            screen.blit(overlay, (0,0))
            

class SceneManager():
    def __init__(self):
        self.scenes = []
    def isEmpty(self):
        return len(self.scenes) == 0
    def enterScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onEnter()
    def exitScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onExit()
    def input(self):
        if len(self.scenes) > 0:
            self.scenes[-1].input(self)
    def update(self):
        if len(self.scenes) > 0:
            self.scenes[-1].update(self)
    def draw(self, screen):
        if len(self.scenes) > 0:
            self.scenes[-1].draw(self,screen)
        #present the screen
        pygame.display.flip()
    def push(self, scene):
        self.exitScene()
        self.scenes.append(scene)
        self.enterScene()
    def pop(self):
       self.exitScene()
       self.scenes.pop()
       self.enterScene()
    def set(self, scene):
        #pop all scenes
        while len(self.scenes) > 0:
            self.pop()
        #add new scene
        self.push(scene)