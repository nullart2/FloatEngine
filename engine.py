#Uses Python with SDL2
#C++ is Not Supported

import pygame

Dark_Purple = (60,50,120)
Black = (50,50,50)

class System():
    def __init__(self):
        pass
    def check(self, entity):
        return True
    def update(self, screen, entities, platforms):
        for entity in entities:
            if self.check(entity):
                self.updateEntity(screen, entity, entities, platforms)
    def updateEntity(self, screen, entity, platforms):
        pass

class CameraSystem(System):
    def __init__(self):
        super().__init__()
    def check(self, entity):
        return entity.camera is not None
    def updateEntity(self, screen, entity, entities, platforms):

        #set clipping rectangle
        cameraRect = entity.camera.rect
        clipRect = pygame.Rect(cameraRect.x, cameraRect.y, cameraRect.w, cameraRect.h)
        screen.set_clip(clipRect)

        #update camera when tracking
        if entity.camera.entityToTrack is not None:
            trackedEntity = entity.camera.entityToTrack

            currentX = entity.camera.worldX
            currentY = entity.camera.worldY

            targetX = trackedEntity.position.rect.x + trackedEntity.position.rect.w/2
            targetY = trackedEntity.position.rect.y + trackedEntity.position.rect.h/2

            entity.camera.worldX = (currentX * 0.90) + (targetX * 0.02)
            entity.camera.worldY = (currentY * 0.90) + (targetY * 0.02)

        #calculate offsets
        offestX = cameraRect.x + cameraRect.w/2 - entity.camera.worldX
        offestY = cameraRect.y + cameraRect.h/2 - entity.camera.worldY

        #fill camera background when there is no map
        if MakeMap == False:
            screen.fill(Black)

        #render platforms
        for p in platforms:
            newPosRect = pygame.Rect(p.x + offestX, p.y + offestY, p.w, p.h)
            pygame.draw.rect(screen, Dark_Purple, newPosRect)

        #calling entities
        for e in entities:
            s = e.state
            a = e.animations.animationList[s]
            #True, False == Hortizontally(true), vertically(false)
            a.draw(screen, e.position.rect.x, e.position.rect.y, e.direction == 'left', False)

        #unset clipping rectangle
        screen.set_clip(None)

class Camera():
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.worldX = 0
        self.worldY = 0
        self.entityToTrack = None
    def setWorldPos (self, x, y):
        self.worldX = x
        self.worldY = y
    def trackEntity(self, e):
        self.entityToTrack = e

class Position():
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

class Animation():
    def __init__(self, imageList):
        self.imageList = imageList
        self.imageIndex = 0
        self.animationTimer = 0 
        self.animationSpeed = 8
    def update(self):
        self.animationTimer += 1
        if self.animationTimer >= self.animationSpeed:
            self.animationTimer = 0
            self.imageIndex += 1
            if self.imageIndex > len(self.imageList) - 1:
                self.imageIndex = 0
    def draw(self, screen, x, y, flipX, flipY):
        screen.blit(pygame.transform.flip(self.imageList[self.imageIndex], flipX, flipY), (x, y))

class Animations():
    def __init__(self):
        self.animationList = {}
    def add(self, state, animation):
        self.animationList[state] = animation

class MakeMap():
    def blit_all_tiles (screen, texdata, world_offset):
        for layer in texdata:
            for tile in layer.tiles():
                x_pixel = tile[0] * 8 + world_offset[0] #FILL Area on X-Axis
                y_pixel = tile[1] * 5 + world_offset[1] #FILL Area on Y-Axis
                screen.blit( tile [2], (x_pixel, y_pixel))

class Entity():
    def __init__(self):
        self.state = 'idle'       
        self.type = 'default'
        self.position = None
        self.animations = Animations()
        self.direction = 'right'
        self.camera = None

