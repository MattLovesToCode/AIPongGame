import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define game objects
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.velocity = [random.choice([-2, 2]), random.choice([-2, 2])]

# Function to draw text on screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Initialize game objects
player_paddle = Paddle(WHITE, 10, 100)
player_paddle.rect.x = 20
player_paddle.rect.y = SCREEN_HEIGHT // 2 - 50

ai_paddle = Paddle(WHITE, 10, 100)
ai_paddle.rect.x = SCREEN_WIDTH - 30
ai_paddle.rect.y = SCREEN_HEIGHT // 2 - 50

ball = Ball(WHITE, 10, 10)
ball.rect.x = SCREEN_WIDTH // 2
ball.rect.y = SCREEN_HEIGHT // 2

all_sprites = pygame.sprite.Group()
all_sprites.add(player_paddle, ai_paddle, ball)

# Game loop
clock = pygame.time.Clock()
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.rect.y > 0:
        player_paddle.rect.y -= 5
    if keys[pygame.K_DOWN] and player_paddle.rect.y < SCREEN_HEIGHT - player_paddle.rect.height:
        player_paddle.rect.y += 5

    # AI controls
    if ball.rect.y < ai_paddle.rect.y:
        ai_paddle.rect.y -= 3
    elif ball.rect.y > ai_paddle.rect.y:
        ai_paddle.rect.y += 3

    # Move the ball
    ball.rect.x += ball.velocity[0]
    ball.rect.y += ball.velocity[1]

    # Bounce the ball off the walls
    if ball.rect.y > SCREEN_HEIGHT - 10 or ball.rect.y < 0:
        ball.velocity[1] = -ball.velocity[1]

    # Check for collisions with paddles
    if pygame.sprite.collide_rect(ball, player_paddle) or pygame.sprite.collide_rect(ball, ai_paddle):
        ball.velocity[0] = -ball.velocity[0]

    # Check if the ball goes out of bounds
    if ball.rect.x > SCREEN_WIDTH or ball.rect.x < 0:
        game_over = True

    # Clear the screen
    screen.fill(BLACK)

    # Draw the game objects
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Game over message
screen.fill(BLACK)
font = pygame.font.Font(None, 36)
draw_text("Game Over", font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
pygame.display.flip()

# Wait for a moment before quitting
pygame.time.wait(2000)

# Quit Pygame
pygame.quit()
