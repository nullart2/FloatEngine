#Uses Python with SDL2
#C++/C# is Not Yet Supported

from typing import Text
import pygame
import engine
import utils
import level
import scene
from pytmx.util_pygame import load_pygame
import pytmx
pytmx.__file__
pytmx.__dir__()

#detect if pygame = true
if pygame:
    print("FloatEngine.Start")

#detect if engine = true
if engine:
    print('Engine.OnLoad') 
    print("FloatEngine.Active") 

#color variables
Screen_Size = (700,500)

#init 
pygame.init()
screen = pygame.display.set_mode(Screen_Size)
pygame.display.set_caption('Float Engine')
pygame_icon = pygame.image.load('D:\SDL2-Engine/assets/EngineLogo.png')
world_offset = [0, 0]
texdata = load_pygame('D:\SDL2-Engine/map_data/world.tmx')

#Fullscreen
fullscreen = True

#game states --> playing/win/lose
game_state = 'playing'

entities = []

#VSync
clock = pygame.time.Clock()

#icon
pygame.display.set_icon(pygame_icon)

#player
player_speed = 0
player_acceleration = 0.3

#coins
coin1 = (utils.makeCoin(100, 200))
coin2 = (utils.makeCoin(200, 270))

#enemies
enemy = utils.makeEnemy(150, 274)

#instantiate player
player = utils.makePlayer(300, 0)
player.camera = engine.Camera(-410, -320, 1000, 800) 
player.camera.setWorldPos(345, 250) #camera fov
player.camera.trackEntity(player) #camera focused on player
player.score = engine.Score()
player.battle = engine.Battle()

#camera system
cameraSys = engine.CameraSystem()

#win/lose conditions:

def lostLevel(level):
#level is not lost if there are lives left
    for entity in level.entities:
        if entity.type == 'player':
            if entity.battle is not None:
                if entity.battle.lives > 0:
                    return False
#lose if no more players/player lives
    return True

#win if no more collectables left
def wonLevel(level):
    for entity in level.entities:
        if entity.type == 'collectable':
        #if there is still a collectable then player has not won yet
                return False
    #won the level
    return True

#scenes
scene1 = level.Level(
    platforms = [
        pygame.Rect(100,300,400,50),
        pygame.Rect(450,250,50,50),
        pygame.Rect(100,250,50,50)
    ],
    entities = [
        player, enemy, coin1, coin2
    ],
    #texdata1 here
    winFunc = wonLevel,
    loseFunc = lostLevel 
)

scene2 = level.Level(
    platforms = [
        pygame.Rect(100,300,400,50),
    ],
    entities = [
        player, enemy
    ],
    #texdata2 here
    winFunc = wonLevel,
    loseFunc = lostLevel 
)

#set scene
sceneManager = scene.SceneManager()
mainMenu = scene.MainMenuScene()
sceneManager.push(mainMenu)

#set world
world = scene1

#running? then start loop
running = True
while running:

#---
#LOOP  
#---
    
    #update display
    pygame.display.update()

    #update map data
    engine.MakeMap.blit_all_tiles(screen, texdata, world_offset)

    #if no map data
    if texdata == None:
        engine.MakeMap == False

    if game_state == 'playing':
        
        #update animations
        for entity in world.entities:
            entity.animations.animationList[entity.state].update()  

        #input  
        new_player_x = player.position.rect.x
        new_player_y = player.position.rect.y

        sceneManager.input()
        sceneManager.update()
        sceneManager.draw()
        
        #left
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            new_player_x -= 2
            player.direction = 'left'
            player.state = 'walking'
        #right
        if keys[pygame.K_d]:
            new_player_x += 2
            player.direction = 'right'
            player.state = 'walking'
        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            player.state = 'idle'
        
        #---IN PROGRESS---#
        #up
        #if keys[pygame.K_d]:
            #new_player_x += 2
            #player.direction = 'right'
            #player.state = 'walking'
        #if not keys[pygame.K_d] and not keys[pygame.K_a]:
            #player.state = 'idle'
        #down
        #if keys[pygame.K_d]:
            #new_player_x += 2
            #player.direction = 'right'
            #player.state = 'walking'
        #if not keys[pygame.K_d] and not keys[pygame.K_a]:
            #player.state = 'idle'
        #up-right
        #if keys[pygame.K_d]:
            #new_player_x += 2
            #player.direction = 'right'
            #player.state = 'walking'
        #if not keys[pygame.K_d] and not keys[pygame.K_a]:
            #player.state = 'idle'
        #down-right
        #if keys[pygame.K_d]:
            #new_player_x += 2
            #player.direction = 'right'
            #player.state = 'walking'
        #if not keys[pygame.K_d] and not keys[pygame.K_a]:
            #player.state = 'idle'
        #up-left
        #if keys[pygame.K_d]:
            #new_player_x += 2
            #player.direction = 'right'
            #player.state = 'walking'
        #if not keys[pygame.K_d] and not keys[pygame.K_a]:
            #player.state = 'idle'
        #down-left
        #if keys[pygame.K_d]:
            #new_player_x += 2
            #player.direction = 'right'
            #player.state = 'walking'
        #if not keys[pygame.K_d] and not keys[pygame.K_a]:
            #player.state = 'idle'
        #---IN PROGRESS --#

        #jump
        if keys[pygame.K_SPACE] and player_on_ground == True:
            player_speed = -7
            #player_state = 'jumping'

        #horizontial Movement
        new_player_rect = pygame.Rect(new_player_x, player.position.rect.y, player.position.rect.width, player.position.rect.height)
        x_collison = False

        #collison Handler X
        for p in world.platforms:
            if p.colliderect(new_player_rect):
                x_collison = True
                break
        
        if x_collison == False:
            player.position.rect.x = new_player_x

        #vertical Movement
        player_speed += player_acceleration
        new_player_y += player_speed

        new_player_rect = pygame.Rect(player.position.rect.x, new_player_y, player.position.rect.width, player.position.rect.height)
        y_collison = False
        player_on_ground = False

        #collison Handler Y
        for p in world.platforms:
            if p.colliderect(new_player_rect):
                y_collison = True
                player_speed = 0
                # if the platform is below the player
                if p[1] > new_player_y:
                    #attach to platform
                    player.position.rect.y = p[1] - player.position.rect.height
                    player_on_ground = True
                break
        
        if y_collison == False:
            player.position.rect.y = new_player_y
        
        #collection system
        player_rect = pygame.Rect(player.position.rect.x, player.position.rect.y, player.position.rect.width, player.position.rect.height)
        for entity in world.entities:
            if entity.type == 'collectable':
                if entity.position.rect.colliderect(player_rect):
                    world.entities.remove(entity)
                    player.score.score += 1
                    #win if score is 2
                    #if player.score.score >= 2:
                        #game_state = 'win'
                        #test level system 
                        #world = level2 
        
        #enemy system
        for entity in world.entities:
            if entity.type == 'enemy':
                if entity.position.rect.colliderect(player_rect):
                    player.battle.lives  -= 1             
                    player.position.rect.x = 300
                    player.position.rect.y = 0
                    player_speed = 0
                    #player death
                    #if player.battle.lives <= 0:
                        #game_state = 'lose'
                        #test level system:
                            #player.battle.lives += 3
                            #world = level1 
        if world.isWon():
            game_state = 'win'
        if world.isLost():
            game_state = 'lose'
        

    #out of bounds collider, use enemy as base

    #check quit
    for event in pygame.event.get():
        if event.type == 256:
            running = False

#---
#UPDATE  
#---
    clock.tick(60)

#---
#RENDER/DRAW
#---
    #background
    #screen.fill(Black)

    cameraSys.update(screen, world)

    if game_state == 'playing':

    #screen
        pygame.display.flip()


#---
#EXIT
#---
pygame.quit()
