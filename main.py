import pygame, os, sys
from pygame.locals import *
pygame.init()
fpsClock = pygame.time.Clock()
# Window Size
wind_x = 600
wind_y = 400
main_surface = pygame.display.set_mode((wind_x, wind_y))
pygame.display.set_caption('Bricks')

color = pygame.Color(0, 0, 0)  # black

# bat init
bat = pygame.image.load('bat.png')
player_y = wind_y - 50
bat_rect = bat.get_rect()
mouse_x, mouse_y = (0, player_y)

# ball init
ball = pygame.image.load('ball.png')
ball_rect = ball.get_rect()
ball_start_y = 200
ball_speed = 5
ball_served = False
ball_x, ball_y = (24, ball_start_y)
speed_x, speed_y = (ball_speed, ball_speed)
ball_rect.topleft = (ball_x, ball_y)

# Hits Counter
hits = 0

# brick init
def create_bricks(path_2_image, rows, cols):
    global brick
    brick = pygame.image.load(path_2_image)
    bricks = []
    for y in range(rows):
        brick_y = y * 16 + 10
        for x in range(cols):
            brick_x = x * 31 + 50
            width = brick.get_width()
            height = brick.get_height()
            rect = Rect(brick_x, brick_y, width, height)
            bricks.append(rect)
    return bricks
bricks = create_bricks('brick.png', 14, 16)

# Deleting All Bricks
def del_bricks():
    bricks = []
    return bricks 

# GAME Loop
while True:
    main_surface.fill(color)
    
    # brick draw
    for brick_rect in bricks:
        main_surface.blit(brick, brick_rect)
    
    # bat and ball draw
    main_surface.blit(bat, bat_rect)
    main_surface.blit(ball, ball_rect)
    
    # events
    for event in pygame.event.get():
        # close window, quit from game
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        # start to serve a ball
        elif event.type == MOUSEBUTTONUP and not ball_served:
            ball_served = True

        # moving bat using mouse X coordinates
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if mouse_x < wind_x - 55:
                bat_rect.topleft = (mouse_x, player_y)
            else:
                bat_rect.topleft = (wind_x - 55, player_y)
    
    # main game logic
    """ The formula to calculate distance is
    Distance = Speed × Time
    Because our rate is fixed to 30 frames per second, we will be adding our
    speed to the current position once every 1/30 of a second. This means that
    after 1 second our ball will have traveled
    30 × 3 = 90 pixels  30(times per second) x 3(pix) = 90(pix)
    So, the actual velocity of our ball is 90 pixels per second. """
    
    # ball moving
    if ball_served:
        ball_x += speed_x
        ball_y += speed_y
        ball_rect.topleft = (ball_x, ball_y)
    
    # changing directions if ball touching any adge
    if ball_y <= 0:         # top of the screen
        ball_y = 0
        speed_y *= -1
    if ball_y >= wind_y - 8:   # bottom of the screen
        ## ball_y = wind_y - 8
        ## speed_y *= -1 
        # resetting yhe ball position
        ball_served = False
        ball_speed = 5
        ball_x, ball_y = (24, ball_start_y)
        speed_x, speed_y = (ball_speed, ball_speed)
        ball_rect.topleft = (ball_x, ball_y)
    if ball_x >= wind_x - 8:   # right side of the screen
        ball_x = wind_x -8
        speed_x *= -1
    if ball_x <=0:          # left side of the screen
        ball_x = 0
        speed_x *= -1
    
    # collision detection
    # ball is touching the bat
    if ball_rect.colliderect(bat_rect):
        ball_y = player_y - 8
        speed_y *= -1
    
    # ball is touching the brick
    brick_hit_index = ball_rect.collidelist(bricks) # gives index of hited brick from bricks (if not gives -1)
    if brick_hit_index >= 0:
        hited_brick = bricks[brick_hit_index]
        ball_middle_x = ball_x + 4
        ball_middle_y = ball_y + 4
        """ We test this middle point of the ball
        against the width of the brick that was hit. If it is outside the width then the
        ball was hit from the side. Otherwise, the ball hit the brick on the top or
        bottom. We deflect the ball accordingly by changing its speed."""
        if ball_middle_x > hited_brick.x + hited_brick.width or ball_middle_x < hited_brick.x:
            speed_x *= -1  # touching from left or right side
        else:
            speed_y *= -1  # touching from top or bottom
        del(bricks[brick_hit_index])
        hits += 1  # counting hits
        if hits == 3:
            bricks = []


    pygame.display.update()
    fpsClock.tick(30)  # 30 frames per second

