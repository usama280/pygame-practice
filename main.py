import pygame
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('FirstGame') 


#CONSTANTS
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

FPS = 60
BULLET_VEL = 7
MAX_BULLETS = 3
VEL = 5                         #x      y   w    h 
MIDDLE_BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGHT) #must sub 5 because width of 10 is 10 to the right!


#creating custom events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


#font and sound
HEALTH_FONT = pygame.font.SysFont('comicsans', 40) #size 40
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/hit.mp3')
BULLET_SOUND = pygame.mixer.Sound('Assets/shoot.mp3')


#Loading/Scaling/Rotating model
YELLOW_SPACESHIP = pygame.image.load('Assets/spaceship_yellow.png')                         #rotate 90 deg
YELLOW_SPACESHIP = pygame.transform.rotate( pygame.transform.scale(YELLOW_SPACESHIP, (55,40)), 90)
                                                          #scales image down                      
RED_SPACESHIP = pygame.image.load('Assets/spaceship_red.png')
RED_SPACESHIP = pygame.transform.rotate( pygame.transform.scale(RED_SPACESHIP, (55,40)), 270)

SPACE = pygame.transform.scale(pygame.image.load('Assets/space.png'), (WIDTH, HEIGHT))



#functions used to draw things onto window
def draw_window(red, yellow, red_bullets, yellow_bullets, red_hp, yellow_hp):
    WINDOW.blit(SPACE, (0,0))
    pygame.draw.rect(WINDOW, BLACK, MIDDLE_BORDER)

    red_hp_txt = HEALTH_FONT.render('Health: ' + str(red_hp), 1, WHITE)
    yellow_hp_txt = HEALTH_FONT.render('Health: ' + str(yellow_hp), 1, WHITE)
    WINDOW.blit(red_hp_txt, (WIDTH-red_hp_txt.get_width() - 10, 10))
    WINDOW.blit(yellow_hp_txt, (10, 10))

    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x,yellow.y)) #0,0 is top left
    WINDOW.blit(RED_SPACESHIP, (red.x,red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    pygame.display.update() #must update after updates



#this handles movement for yellow spaceship
def yellow_move(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x -VEL > 0: #returns 0 or 1 (checking for left key here)
            yellow.x -= VEL
    if keys_pressed[pygame.K_d] and (yellow.x +VEL + yellow.width) < MIDDLE_BORDER.x: #right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y -VEL > 0: #up
        yellow.y -= VEL #remember to left is 0,0 so to go up we need to sub
    if keys_pressed[pygame.K_s] and (yellow.y +VEL + yellow.height) < HEIGHT: #down
        yellow.y += VEL



#This handles movement for red spaceship
def red_move(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x -VEL > MIDDLE_BORDER.x + MIDDLE_BORDER.width: #left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and (red.x +VEL + red.width) < WIDTH: #right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y -VEL > 0: #up
        red.y -= VEL 
    if keys_pressed[pygame.K_DOWN] and (red.y +VEL + red.height) < HEIGHT: #down
        red.y += VEL



#handles bullets
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL

        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT)) #call event
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL

        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)



#prints winner
def draw_winner(text):
    WIN_FONT = pygame.font.SysFont('comicsans', 100).render(text, 1, WHITE)
    WINDOW.blit(WIN_FONT, (WIDTH//2 - WIN_FONT.get_width()//2, HEIGHT//2 - WIN_FONT.get_height()//2))

    pygame.display.update()
    pygame.time.delay(5000)



#main function
def main():
                      #pos    #spaceship h and w
    red = pygame.Rect(700,300, 40, 55) # w and h is switched because when we rotated the img, it cause the w to become the h
    yellow = pygame.Rect(100, 300, 40, 55)
    clock = pygame.time.Clock() #needed to cap fps
    run = True
    
    red_bullets = []
    yellow_bullets = []
    yellow_hp = 10
    red_hp = 10

    while run:
        clock.tick(FPS)
        for event in pygame.event.get(): #handles quit on exit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10,5)
                    yellow_bullets.append(bullet)
                    BULLET_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10,5)
                    red_bullets.append(bullet)
                    BULLET_SOUND.play()

            if event.type == RED_HIT:
                red_hp -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_hp -= 1
                BULLET_HIT_SOUND.play()
        
        winner = ''
        if red_hp  <= 0:
            winner = 'Yellow Wins!'
        if yellow_hp <= 0:
            winner = 'Red Wins!'

        if winner:
            draw_winner(winner)
            break

        keys_pressed = pygame.key.get_pressed() #checks what keys are being pressed
        yellow_move(keys_pressed, yellow)
        red_move(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_hp, yellow_hp)

    #quit or restart
    #pygame.quit()
    main()



if __name__ == '__main__':
    main()