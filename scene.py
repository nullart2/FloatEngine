#Uses Python with SDL2
#C++/C# is Not Yet Supported

from logging import setLogRecordFactory
import pygame

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
    def draw(self, sm):
        pass

class MainMenuScene(Scene):
    def onEnter(self):
        print('entering menu')
    def onExit(self):
        print('exiting menu')
    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            sm.push(LevelSelectScene())
        if keys[pygame.K_F1]:
            #quit game completely
            sm.pop()
    def update(self, sm):
        pass
    def draw(self, sm):
        pass

class LevelSelectScene(Scene):
    def onEnter(self):
        print('entering lvl select')
    def onExit(self):
        print('exiting lvl select')
    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            sm.push(GameScene())
        if keys[pygame.K_2]:
            sm.push(GameScene())
        if keys[pygame.K_ESCAPE]:
            sm.pop()
    def update(self, sm):
        pass
    def draw(self, sm):
        pass

class GameScene(Scene):
    def onEnter(self):
        print('entering game')
    def onExit(self):
        print('exiting game')
    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sm.pop()
    def update(self, sm):
        pass
    def draw(self, sm):
        pass


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
    def draw(self):
        if len(self.scenes) > 0:
            self.scenes[-1].draw(self)
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