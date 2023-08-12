#import the needed modules and classes
import pygame
import math
from random import randint
from pygame import mixer
pygame.init()
#specify some variables 
height=600
width=800 
running=True
score=0
high_score=0
fire=False
endgame=False
replay=""
#create the screen and background image and music and blit the background in the main game loop
screen=pygame.display.set_mode((width,height))
icon=pygame.image.load("game_files/player.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Space invaders by Deciphrexx")
background_img=pygame.image.load("game_files/background.png")
mixer.music.load("game_files/background.wav")
mixer.music.play(-1)
#specify the things that will appear on the screen
#player
player_img=pygame.image.load("game_files/player2.png")
xP=width*0.5-32       ;dxP=0
yP=height-120         ;dyP=0
#multiple enemies
enemy_img=[]
xE=[]     ;dxE=[]
yE=[]     ;dyE=[]
num_enemies=10
for i in range(num_enemies):
    enemy_img.append(pygame.image.load("game_files/enemy.png"))
    xE.append(randint(1,width-64))         ;dxE.append(5)
    yE.append(randint(1,height*0.33))       ;dyE.append(70)
#bullet
bullet_img=pygame.image.load("game_files/bullet.png")
xB=0        ;dxB=0
yB=0        ;dyB=-40
#the font
font=pygame.font.Font(None,40)
over_font=pygame.font.Font(None,100)

#define the functions (create a function for almost everything that happens on the screeni.e the player moving,the enemy moving showing the score,e.t.c)
def player(x,y):
    screen.blit(player_img ,(x,y))
def enemy(x,y):
    screen.blit(enemy_img[i],(x,y))
def bullet(x,y):
    screen.blit(bullet_img,(x+16,y+14)) 
def iscollision(xE,yE,xB,yB):
    distance=math.sqrt(math.pow(xE-xB,2)+math.pow(yE-yB,2))
    if distance<28:
        return True
    else: return False
def show_score():
    score_text=font.render(f" Enemy_Kills :{score}                                  High_Score :{high_score} Kills",True,(255,255,255))
    screen.blit(score_text,(10,10))
def game_over():
    game_over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(game_over_text,(180,250))
#the main game loop
while running:
    #fill the screen to avoid the previous images from being visible when the images move
    screen.fill((0,0,0))
    #blit out the background image
    screen.blit(background_img,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            # define what you want to happen when certain keys are pressed
            if event.key==pygame.K_x:
                running=False
            if event.key==pygame.K_LEFT:
                dxP=-10
            if event.key==pygame.K_RIGHT:
                dxP=10
            if event.key==pygame.K_UP:
                dyP=-10
            if event.key==pygame.K_DOWN:
                dyP=10
            if event.key==pygame.K_SPACE:
                fire=True
            if event.key==pygame.K_HOME:
                replay=True
                endgame=False
        if event.type == pygame.KEYUP :
            # also remember to define what you want to happen when the keys are released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key==pygame.K_UP or event.key==pygame.K_DOWN :
                dxP = 0
                dyP=0 
            if event.key==pygame.K_HOME:
                replay=False
    # define that if the bullet is not in a state of fire, the bullet should copy the  player's coordinates
    if not fire:
        xB=xP 
        yB=yP
    #define that if the bullet is in a state of fire, the bullet should move upwards and also that the bullet should play a sound at the correct moment 
    if fire:
        if yB >yP-5:
            bullet_sound=mixer.Sound("game_files/laser.wav")
            bullet_sound.play()
        #I can use += because I made dyB a negative value
        yB+=dyB
    #this puts the bullet's fire in  false state when the bullet leaves the top of the screen
    if yB<0:
        fire=False
    #now print out the bullet
    bullet(xB,yB)
    #increment or decrement the player's position as defined by the pressed keys
    xP+=dxP ;yP+=dyP            
    if xP<=0:           xP=0#to not let it go beyond the left boundary
    elif xP>=width-64:  xP=width-64#to not let it go beyond the right boundary
    #to print out the player
    player(xP,yP)
    #put everything concerning the enemy(ies) in here
    #the '[i]' refers to a particular enemy and the main thing differentiating the enemies is the randint class defining their respective initial positions
    for i in range(num_enemies):
        #if the player touches the enemy
        if yE[i]>=yP-48 and yE[i]<=yP+50 and xE[i]>=xP-36 and xE[i]<=xP+48:
            #to move all the enemies far downward
            for j in range(num_enemies):
                yE[j]=2000
                endgame=True
        #to keep the enemy moving
        xE[i]+=dxE [i] 
        #to print out the movement
        enemy(xE[i],yE[i])
        #when the enemies reach the boundaries
        if xE[i]>width-60 or xE[i]<0:
            #the enemy changes direction
            dxE[i]*=-1
            #the enemy moves down a bit
            yE[i]+=dyE[i]
        #I am attributing the proceeds of the iscollision function to the variable 'collision'
        collision=iscollision(xE[i],yE[i],xB,yB)
        #define what you want to happen if the bullet and enemy collide
        if collision: 
            #increment the high score only if the score is up to the high score 
            if score==high_score:
                high_score+=1
            #increment the score
            score+=1
            explosion_sound=mixer.Sound("game_files/explosion.wav")
            explosion_sound.play()
            fire=False
            xE[i]=randint(1,width-64)
            yE[i]=randint(1,height*0.33)
    #remember to display the score
    show_score()
    
    #if the variable endgame is set to true when the player touches the enemy,refer to the game_over function defined previously
    if endgame:
        game_over()
    if replay:
        for i in range(num_enemies):
            #to bring back the enemies to view            
            xE[i]=randint(1,width-64)
            yE[i]=randint(1,height*0.5)
            #reset the score only and not also the high score
            score=0
    #VERY IMPORTANTLY UPDATE THE GAME 
    pygame.display.update()