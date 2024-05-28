import pygame
import random
import sys

pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Falling Alphabet Game")

# 색상 설정
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# 폰트 설정
font = pygame.font.Font(None, 74)

# 알파벳 설정
alphabet = ""
alphabet_pos = [screen_width // 2, screen_height // 2]
alphabet_velocity = [0, 0]

# 장애물 설정
obstacles = []
for _ in range(5):
    x = random.randint(0, screen_width - 50)
    y = random.randint(0, screen_height - 50)
    obstacles.append(pygame.Rect(x, y, 50, 50))

# 게임 루프
clock = pygame.time.Clock()
running = True
falling = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and alphabet:
                falling = True
                alphabet_velocity = [random.choice([-3, 3]), 5]
            elif event.key == pygame.K_BACKSPACE:
                alphabet = alphabet[:-1]
            elif event.unicode.isalpha():
                alphabet = event.unicode.upper()

    if falling:
        alphabet_pos[0] += alphabet_velocity[0]
        alphabet_pos[1] += alphabet_velocity[1]

        # 화면 경계에 튕기기
        if alphabet_pos[0] <= 0 or alphabet_pos[0] >= screen_width:
            alphabet_velocity[0] = -alphabet_velocity[0]
        if alphabet_pos[1] <= 0 or alphabet_pos[1] >= screen_height:
            alphabet_velocity[1] = -alphabet_velocity[1]

        # 장애물에 부딪히면 튕기기
        alphabet_rect = pygame.Rect(alphabet_pos[0], alphabet_pos[1], 50, 50)
        for obstacle in obstacles:
            if alphabet_rect.colliderect(obstacle):
                alphabet_velocity[0] = -alphabet_velocity[0]
                alphabet_velocity[1] = -alphabet_velocity[1]

    # 화면 그리기
    screen.fill(black)
    
    if alphabet:
        text = font.render(alphabet, True, white)
        screen.blit(text, alphabet_pos)

    for obstacle in obstacles:
        pygame.draw.rect(screen, red, obstacle)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()

