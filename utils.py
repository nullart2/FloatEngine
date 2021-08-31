#Uses Python with SDL2
#C++/C# is Not Yet Supported

import pygame
import engine

#colors
Dark_Purple = (60,50,120)
Black = (50,50,50)
White = (210,200,201)

#font(s)
pygame.font.init()
font = pygame.font.Font(('D:\SDL2-Engine/fonts/munro.ttf'), 22) 

#images
coin_image = pygame.image.load('D:\SDL2-Engine/images/coin_0.png')
heart_image = pygame.image.load('D:\SDL2-Engine/images/heart.png')

#draw text
def drawText(screen, t, x, y):
    text = font.render(t, True, White)
    text_rectangle = text.get_rect()
    text_rectangle.topleft = (x,y)
    screen.blit(text, text_rectangle)

def makeCoin(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 23, 23)
    entityAnimation = engine.Animation([
        pygame.image.load('D:\SDL2-Engine/images/coin_0.png'),
        pygame.image.load('D:\SDL2-Engine/images/coin_1.png'),
        pygame.image.load('D:\SDL2-Engine/images/coin_2.png'),
        pygame.image.load('D:\SDL2-Engine/images/coin_3.png'),
        pygame.image.load('D:\SDL2-Engine/images/coin_4.png'),
        pygame.image.load('D:\SDL2-Engine/images/coin_5.png')
    ])
    entity.animations = engine.Animations()
    entity.animations.add('idle', entityAnimation)
    entity.type = 'collectable'
    return entity

enemy0 = pygame.image.load('D:\SDL2-Engine/images/spike_monster.png')

def makeEnemy(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 30, 30)
    entityAnimation = engine.Animation([enemy0])
    entity.animations = engine.Animations()
    entity.animations.add('idle', entityAnimation)
    entity.type = 'enemy'
    return entity



idle0 = pygame.image.load('D:\SDL2-Engine/images/character_00.png')
idle1 = pygame.image.load('D:\SDL2-Engine/images/character_01.png')
idle2 = pygame.image.load('D:\SDL2-Engine/images/character_02.png')
idle3 = pygame.image.load('D:\SDL2-Engine/images/character_03.png')


walking0 = pygame.image.load('D:\SDL2-Engine/images/character_04.png')
walking1 = pygame.image.load('D:\SDL2-Engine/images/character_05.png')
walking2 = pygame.image.load('D:\SDL2-Engine/images/character_06.png')
walking3 = pygame.image.load('D:\SDL2-Engine/images/character_07.png')
walking4 = pygame.image.load('D:\SDL2-Engine/images/character_08.png')
walking5 = pygame.image.load('D:\SDL2-Engine/images/character_09.png')

def makePlayer(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 45, 51)
    entityIdleAnimation = engine.Animation([idle0, idle1, idle2, idle3])
    entityWalkingAnimation = engine.Animation([walking0, walking1, walking2, walking3, walking4, walking5])
    entity.animations = engine.Animations()
    entity.animations.add('idle', entityIdleAnimation)
    entity.animations.add('walking', entityWalkingAnimation)
    entity.type = 'player'
    return entity




