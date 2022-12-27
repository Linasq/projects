import random
import pygame

score=0
endTime=0

def collisions(bird, t1, t2):
    if t1:
        for rect in t1:
            if bird.colliderect(rect): return False
        for rect in t2:
            if bird.colliderect(rect): return False
    if bird_rect.bottom>=350: return False
    return True

def displayScore():
    global score
    score = (pygame.time.get_ticks() // 2000) - endTime
    scoreM = font.render(f'Score: {score}', False, 'black')
    scoreM_rect = scoreM.get_rect(topleft=(0, 0))
    screen.blit(scoreM, scoreM_rect)

def tube_move(t1, t2):
    if t1:
        for i in range(len(t1)):
            t1[i].x-=4
            t2[i].x-=4

            screen.blit(tube1_surf, t1[i])
            screen.blit(tube2_surf, t2[i])
        t1=[i for i in t1 if i.x>=-100]
        t2=[i for i in t2 if i.x>=-100]
        return t1,t2
    else: return [], []

#starting game
pygame.init()
screen=pygame.display.set_mode((800,400))
pygame.display.set_caption('Flappy Bird')
clock=pygame.time.Clock()

#font
font=pygame.font.Font('font/Pixeltype.ttf', 50)
fontGG=pygame.font.Font('font/Pixeltype.ttf', 100)

#surface background
bg_surf=pygame.image.load('grafika/bg.png').convert()
bg_surf=pygame.transform.scale2x(bg_surf)
bg_rect=bg_surf.get_rect(center=(0,0))

ground_surf=pygame.image.load('grafika/ground.png').convert_alpha()
ground_surf=pygame.transform.smoothscale(ground_surf, (800,200))
ground_rect=ground_surf.get_rect(midtop=(400, 350))

#Bird
bird_surf=pygame.image.load('grafika/bird.png').convert_alpha()
bird_surf=pygame.transform.smoothscale(bird_surf,(48,34))
bird_rect=bird_surf.get_rect(bottomleft=(50,175))

#tube
tube1_surf=pygame.image.load('grafika/tube.png').convert_alpha()
tube1_surf=pygame.transform.smoothscale(tube1_surf, (60,200))
tube1_rect=tube1_surf.get_rect(midtop=(800, 300))
tubes1=[]

tube2_surf=pygame.transform.rotate(tube1_surf, 180)
tube2_rect=tube2_surf.get_rect(midbottom=(800,tube1_rect.y-150))
tubes2=[]

#messages
gameM=font.render('Prace Space to start', False, 'black')
gameM_rect=gameM.get_rect(center=(400,350))

gameName=fontGG.render('Flappy Bird', False, 'black')
gameName_rect=gameName.get_rect(center=(400,200))

#timer
tube_timer=pygame.USEREVENT+1
pygame.time.set_timer(tube_timer, 1500)

gravity=0
game_active=False

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE  and game_active:
                gravity=-13
            if event.key==pygame.K_SPACE and not game_active:
                endTime=pygame.time.get_ticks()//2000
                game_active=True
                gravity=-13
        if game_active:
            if event.type==tube_timer:
                x=random.randint(900,1100)
                y=random.randint(180,330)
                tubes1.append(tube1_surf.get_rect(midtop=(x, y)))
                tubes2.append(tube2_surf.get_rect(midbottom=(x,y-150)))

    if game_active:
        #display bg
        screen.blit(bg_surf,bg_rect)

        #bird
        gravity+=0.9
        bird_rect.y+=gravity
        screen.blit(bird_surf, bird_rect)

        #tube
        tubes1, tubes2 = tube_move(tubes1, tubes2)
        screen.blit(ground_surf, ground_rect)

        #score
        displayScore()

        #collisions
        game_active=collisions(bird_rect, tubes1, tubes2)

    else:
        pygame.time.wait(1000)
        screen.blit(bg_surf, bg_rect)
        bird_rect.y=175
        screen.blit(bird_surf, bird_rect)
        screen.blit(gameName,gameName_rect)
        screen.blit(ground_surf, ground_rect)
        gravity=0
        tubes1.clear()
        tubes2.clear()
        if score !=0:
            scoreM = font.render(f'Your score: {score}', False, 'black')
            scoreM_rect = scoreM.get_rect(center=(400, 350))
            screen.blit(scoreM, scoreM_rect)
        else:
            screen.blit(gameM, gameM_rect)

    pygame.display.update()
    clock.tick(60)