#Uses Python with SDL2
#C++ is Not Supported

from typing import Text
import pygame
import engine
import utils
from pytmx.util_pygame import load_pygame
import pytmx
pytmx.__file__
pytmx.__dir__()

#detect if pygame = true
if pygame:
    print("FloatEngine.Start")
    print("FloatEngine.Active") 

#detect if engine = true
if engine:
    print('Engine.OnLoad') 

#draw text
def drawText(t, x, y):
    text = font.render(t, True, White)
    text_rectangle = text.get_rect()
    text_rectangle.topleft = (x,y)
    screen.blit(text, text_rectangle)

#color variables
Screen_Size = (700,500)
White = (210,200,201)

#init 
pygame.init()
screen = pygame.display.set_mode(Screen_Size)
pygame.display.set_caption('Float Engine')
pygame_icon = pygame.image.load('D:\SDL2-Engine/assets/EngineLogo.png')
font = pygame.font.Font(('D:\SDL2-Engine/fonts/munro.ttf'), 20) 
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

#platforms
platforms = [
    pygame.Rect(100,300,400,50),
    pygame.Rect(450,250,50,50),
    pygame.Rect(100,250,50,50)
]

#coins
coin_image = pygame.image.load('D:\SDL2-Engine/images/coin_0.png')
entities.append(utils.makeCoin(100, 200))
entities.append(utils.makeCoin(200, 270))
score = 0

#enemies
enemy = utils.makeEnemy(150, 274)
entities.append(enemy)

#player instantiate
player = utils.makePlayer(300, 0)
player.camera = engine.Camera(0, 0, 700, 500) 
player.camera.setWorldPos(345, 250) #camera fov
player.camera.trackEntity(player) #camera focused on player
entities.append(player)

#camera system
cameraSys = engine.CameraSystem()

#health
lives = 3
heart_image = pygame.image.load('D:\SDL2-Engine/images/heart.png')

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

        new_player_x = player.position.rect.x
        new_player_y = player.position.rect.y
        
        #update animations
        for entity in entities:
            entity.animations.animationList[entity.state].update()

        #input  
        new_player_x = player.position.rect.x
        new_player_y = player.position.rect.y

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
        for p in platforms:
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
        for p in platforms:
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

        for entity in entities:
            if entity.type == 'collectable':
                if entity.position.rect.colliderect(player_rect):
                    entities.remove(entity)
                    score += 1
                    #win if score is 2
                    if score >= 2:
                        #game_state = 'win'
                        game_state = 'win'
        
        #enemy system
        for entity in entities:
            if entity.type == 'enemy':
                if entity.position.rect.colliderect(player_rect):
                    lives -= 1             
                    player.position.rect.x = 300
                    player.position.rect.y = 0
                    player_speed = 0
                    #player death
                    if lives <= 0:
                        #game_state = 'lose'
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

    cameraSys.update(screen, entities, platforms)

    if game_state == 'playing':

        #scoreText
        #screen.blit(coin_image, (620, 18))
        #drawText(str(score), 660, 22)

        #lives count
        #for l in range(lives):
            #screen.blit(heart_image, (10 + (l * 50), 10))


    #win       
    #if game_state == 'win':
        #drawText('You Win!', 315 , 220)
    #lose
    #if game_state == 'lose':
        #drawText('You Lose!', 315 , 220)

    #screen
        pygame.display.flip()




#---
#EXIT
#---
pygame.quit()
