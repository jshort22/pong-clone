# IMPORTS
import pygame
import os
import sys
import random

# INIT
pygame.init()
pygame.font.init()
pygame.mixer.init()

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# SCREEN
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
# REMINDER: MUST HAVE SOUND EFFECT FOLDER IN VSC FOR FILE TO RUN

# DIVIDER
DIVIDER_WIDTH = 5
DIVIDER = pygame.Rect(SCREEN_WIDTH / 2 - DIVIDER_WIDTH, 0, DIVIDER_WIDTH, SCREEN_HEIGHT)

# PLAYER 1
P1_VEL = 6
P1_WIDTH = 12
P1_HEIGHT = 60
P1 = pygame.Rect(50, SCREEN_HEIGHT / 2 - P1_HEIGHT / 2, P1_WIDTH, P1_HEIGHT)

# PLAYER 2
P2_VEL = 6
P2_WIDTH = 12
P2_HEIGHT = 60
P2 = pygame.Rect(
    SCREEN_WIDTH - 50, SCREEN_HEIGHT / 2 - P2_HEIGHT / 2, P2_WIDTH, P2_HEIGHT
)

# BALL
BALL_VEL_X = 3
BALL_VEL_Y = 3.5
BALL_WIDTH = 10
BALL_HEIGHT = 10
MAX_BALL_SPEED_X = 15
MAX_BALL_SPEED_Y = 7
BALL = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BALL_WIDTH, BALL_HEIGHT)
SOUND_EFFECT = pygame.mixer.Sound(os.path.join("sound_effects", "sound.wav"))

# COUNTERS
VOLLEY_COUNTER = 0
P1_SCORE = 0
P2_SCORE = 0


# FUNCTIONS
def update_score():
    global P1_SCORE, P2_SCORE, BALL_VEL_X, BALL_VEL_Y

    # FONT
    SCORE_FONT = pygame.font.SysFont("roboto", 40)

    # PRINTING SCORE...

    # P1 SCORE TEXT
    p1_score_text = SCORE_FONT.render("Comp: " + str(P1_SCORE), 1, WHITE)
    SCREEN.blit(p1_score_text, (200, 25))

    # P2 SCORE TEXT
    p2_score_text = SCORE_FONT.render("Human: " + str(P2_SCORE), 1, WHITE)
    SCREEN.blit(p2_score_text, (700, 25))

    # PRINT WINNER
    if P1_SCORE >= 11:
        p1_winner_text = SCORE_FONT.render("Computer wins!", 1, WHITE)
        SCREEN.blit(p1_winner_text, (SCREEN_WIDTH / 2 - 90, SCREEN_HEIGHT / 2))
        BALL_VEL_X = 0
        BALL_VEL_Y = 0

    elif P2_SCORE >= 11:
        p2_winner_text = SCORE_FONT.render("Human wins!", 1, WHITE)
        SCREEN.blit(p2_winner_text, (SCREEN_WIDTH / 2 - 90, SCREEN_HEIGHT / 2))
        BALL_VEL_X = 0
        BALL_VEL_Y = 0

    pygame.display.update()


def update_screen():
    SCREEN.fill(BLACK)
    pygame.draw.rect(SCREEN, WHITE, DIVIDER)
    pygame.draw.rect(SCREEN, WHITE, P1)
    pygame.draw.rect(SCREEN, WHITE, P2)
    pygame.draw.rect(SCREEN, GREEN, BALL)
    update_score()
    pygame.display.update()


def ball_movement():

    # initialization
    global BALL_VEL_X, BALL_VEL_Y, P1_SCORE, P2_SCORE, SOUND_EFFECT
    BALL.x -= BALL_VEL_X
    BALL.y -= BALL_VEL_Y

    # ball meets paddle
    if BALL.colliderect(P1) or BALL.colliderect(P2):
        BALL_VEL_X *= -1
        SOUND_EFFECT.play()
        if BALL_VEL_X > 0 and BALL_VEL_X < MAX_BALL_SPEED_X:
            BALL_VEL_X += random.uniform(0.8, 1.2)
        if BALL_VEL_X < 0 and abs(BALL_VEL_X) < MAX_BALL_SPEED_X:
            BALL_VEL_X -= random.uniform(0.8, 1.2)

        if BALL_VEL_Y > 0 and BALL_VEL_Y < MAX_BALL_SPEED_Y:
            BALL_VEL_Y += 0.5
        if BALL_VEL_Y < 0 and abs(BALL_VEL_Y) < MAX_BALL_SPEED_Y:
            BALL_VEL_Y -= 0.5

    # ball meets wall
    if BALL.top < 0 or BALL.bottom > SCREEN_HEIGHT:
        BALL_VEL_Y *= -1

    # P1 scores a point
    if BALL.right - BALL_WIDTH > SCREEN_WIDTH:
        P1_SCORE += 1
        pygame.time.delay(2000)
        BALL.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        reset_ball_speed()

    # P2 scores a point
    global P2_SCORE
    if BALL.left + BALL_WIDTH < 0:
        P2_SCORE += 1
        pygame.time.delay(2000)
        BALL.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        reset_ball_speed()


def reset_ball_speed():
    global BALL_VEL_X, BALL_VEL_Y
    BALL_VEL_X = 3
    BALL_VEL_Y = 1.5
    BALL_VEL_X *= -1
    BALL_VEL_Y *= -1


def computer_movement():
    global P1_VEL
    if P1.centery < BALL.centery and P1.bottom < SCREEN_HEIGHT:
        P1.y += P1_VEL

    if P1.centery > BALL.centery and P1.top > 0:
        P1.y -= P1_VEL


def player_movement():
    global P1_VEL
    global P2_VEL

    keys_pressed = pygame.key.get_pressed()

    """if keys_pressed[pygame.K_w] and P1.y - P1_VEL > 0: #P1 UP
        P1.y -= P1_VEL
    
    if keys_pressed[pygame.K_s] and P1.y + P1_HEIGHT + P1_VEL < SCREEN_HEIGHT: #P1 DOWN
        P1.y += P1_VEL"""

    if keys_pressed[pygame.K_UP] and P2.top > 0:  # P2 UP
        P2.y -= P2_VEL

    if keys_pressed[pygame.K_DOWN] and P2.bottom < SCREEN_HEIGHT:  # P2 DOWN
        P2.y += P2_VEL


def main():

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player_movement()
        computer_movement()
        ball_movement()
        update_screen()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
