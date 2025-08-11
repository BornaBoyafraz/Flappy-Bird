#Flappy Bird
#press Q or Esc to Quit

#LIB
import random
import pygame

pygame.init()


HEIGHT = 600
WIDTH = 900
pygame.display.set_caption("Flappy Space")
#VAR Color
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
red = (55 , 0 , 0)
yellow = (255, 255, 0)

icone = pygame.image.load('Flappy-Bird/Bird.png')
pygame.display.set_icon(icone)


fps = 60
fonts = pygame.font.SysFont('cambria', 20)


#VAR 
player_x = 225
player_y = 225
y_change = 0
jump_height = 12
gravity = .9
obstacles = [400, 700, 1000, 1300, 1600]
generate_places = True
y_positions = []
game_over  = False
speed = 3
score = 0
high_score = 0
stars = []
running  = True


#def

def draw_player(x_pos, y_pos):
    global y_change 
    mouth = pygame.draw.circle(screen, gray, (x_pos + 25, y_pos + 15), 12)
    play = pygame.draw.rect(screen, white, [x_pos, y_pos, 30, 30], 0, 12)
    eye =  pygame.draw.circle(screen, black, (x_pos + 24, y_pos + 12), 5)
    jetpack = pygame.draw.rect(screen, white, [x_pos - 20, y_pos, 18, 28] ,3, 2)
    if y_change < 0:
        flame1 = pygame.draw.rect(screen, red, [x_pos - 20, y_pos + 29, 7, 20] , 0, 2)
        flame1_yellow = pygame.draw.rect(screen, yellow, [x_pos - 18, y_pos + 29, 3, 18] , 0, 2)
        flame2 = pygame.draw.rect(screen, red, [x_pos - 10, y_pos + 29, 7, 20] , 0, 2)
        flame2_yellow = pygame.draw.rect(screen, yellow, [x_pos - 8, y_pos + 29, 3, 18] , 0, 2)
    return play
 

def draw_obstacles(obst, y_pos, play):
    global game_over
    for i in range(len(obst)):
        y_coard = y_pos[i]
        top_rect = pygame.draw.rect(screen , gray, [obst[i], 0, 30, y_coard])
        top2 = pygame.draw.rect(screen , gray ,[obst[i] - 3, y_coard - 20, 36, 20] , 0, 5)
        bot_rect = pygame.draw.rect(screen , gray, [obst[i], y_coard + 200, 30,HEIGHT - (y_coard + 70)])
        bot2 = pygame.draw.rect(screen , gray, [obst[i] - 3, y_coard - 20, 36, 20] , 0, 5)
        if top_rect.colliderect(player) or bot_rect.colliderect(player):
            game_over = True
            #Play_Music('die.mp3', 0.2)


def draw_stars(stars):
    global total
    for i in range(total-1):
        pygame.draw.rect(screen, white, [stars[i][0], stars[i][1], 3, 3,], 0, 2)
        stars[i][0] -= 0.5
        if stars[i][0] < -3:
            stars[i][0] = WIDTH + 3
            stars[i][1] = random.randint(0, HEIGHT)
    return stars



def Play_Music(Musix_name, Volume):
    pygame.mixer.init()
    pygame.mixer.music.load(Musix_name)
    pygame.mixer.music.set_volume(Volume)
    pygame.mixer.music.play()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
timer = pygame.time.Clock()


while running:
    timer.tick(fps)
    screen.fill(black)


    if generate_places:
        for i in range(len(obstacles)):
            y_positions.append(random.randint(0 , 300))
        total = 100
        for i in range(total):
            x_pos = random.randint(0, WIDTH)
            y_pos = random.randint(0, HEIGHT)
            stars.append([x_pos, y_pos])
        

        generate_places = False

    draw_stars(stars)
    player = draw_player(player_x, player_y)
    draw_obstacles(obstacles, y_positions, player)
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and not game_over:
                y_change =- jump_height
                Play_Music('Flappy-Bird/wing.mp3' , 1)
            if event.key == pygame.K_SPACE and score == score + 1 :
                Play_Music('Flappy-Bird/point.mp3', 1)
            if event.key == pygame.K_SPACE and game_over:
                Play_Music('Flappy-Bird/die.mp3', 1)
                player_y = 225
                player_x = 225
                y_change = 0 
                generate_places = True
                obstacles = [400, 700, 100, 1300, 1600]
                y_positions = []
                game_over = False
                score = 0
            # Ask
            if score == score + 1 and event.key == pygame.K_SPACE:
                Play_Music('Flappy-Bird//wing.mp3')
                
    
    if player_y + y_change < HEIGHT - 30:
        player_y += y_change
        y_change += gravity
    else :
        player_y = HEIGHT -30
    

    for i in range(len(obstacles)):
        if not game_over:
            obstacles[i] -= speed
            if obstacles[i] < -30:
                obstacles.remove(obstacles[i])
                y_positions.remove(y_positions[i])
                obstacles.append(random.randint(obstacles[-1] + 280, obstacles[-1] + 320))
                y_positions.append(random.randint(0, 300))
                score +=1
                Play_Music('Flappy-Bird/point.mp3', 1)
    

    if player_y + y_change > HEIGHT - 30:
        game_over = True
    
    if score > high_score:
        high_score = score
    
    if game_over:
        game_over_text = fonts.render('Gamo Over! Press "Space" To Restart, Press "Q" to QUIT.' ,True , white)
        screen.blit(game_over_text , (200, 200))
    
    
    score_text = fonts.render('Score: ' + str(score), True, white)
    screen.blit(score_text, (10, 450))
    high_score_text = fonts.render('High Score: ' + str(high_score), True, white)
    screen.blit(high_score_text, (10, 470))

     

    pygame.display.flip()
pygame.quit()

