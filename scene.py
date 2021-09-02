#Uses Python with SDL2
#C++/C# is Not Yet Supported

import pygame

class Scene():
    def __init__(self):
        pass
    def input(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass

class MainMenuScene(Scene):
    def input(self):
        print("Main Menu Input")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            SceneManager.push()
    def update(self):
        print("Main Menu Update")
    def draw(self):
        print("Main Menu Draw")

class LevelSelect(Scene):
    def input(self):
        print("Level Select Input")
    def update(self):
        print("Level Select Update")
    def draw(self):
        print("Level Select Draw")

class GameScene(Scene):
    pass

class SceneManager():
    def __init__(self):
        self.scenes = []
    def input(self):
        if len(self.scenes) > 0:
            self.scenes[-1].input()
    def update(self):
        if len(self.scenes) > 0:
            self.scenes[-1].update()
    def draw(self):
        if len(self.scenes) > 0:
            self.scenes[-1].draw()
    def push(self, scene):
        self.scenes.append(scene)
    def pop(self):
        self.scenes.pop()
    def set(self, scene):
        self.scenes = [scene]