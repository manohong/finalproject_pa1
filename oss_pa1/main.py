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

# 알파벳 줄 설정
alphabet_line = []
falling_lines = []

# 장애물 설정
obstacles = []
for _ in range(5):
    x = random.randint(0, screen_width - 50)
    y = random.randint(screen_height // 2, screen_height - 50)
    obstacles.append(pygame.Rect(x, y, 50, 50))

# 게임 루프
clock = pygame.time.Clock()
running = True

class Alphabet:
    def __init__(self, char, x, y):
        self.char = char
        self.pos = [x, y]
        self.velocity = [random.choice([-3, 3]), 5]
        self.surface = font.render(char, True, white)

    def update(self):
        self.pos[1] += self.velocity[1]
        self.pos[0] += self.velocity[0]

        # 화면 경계에 튕기기
        if self.pos[0] <= 0 or self.pos[0] >= screen_width - self.surface.get_width():
            self.velocity[0] = -self.velocity[0]
        if self.pos[1] <= 0 or self.pos[1] >= screen_height - self.surface.get_height():
            self.velocity[1] = -self.velocity[1]

        # 장애물에 부딪히면 튕기기
        alphabet_rect = pygame.Rect(self.pos[0], self.pos[1], self.surface.get_width(), self.surface.get_height())
        for obstacle in obstacles:
            if alphabet_rect.colliderect(obstacle):
                self.velocity[0] = -self.velocity[0]
                self.velocity[1] = -self.velocity[1]

    def draw(self, screen):
        screen.blit(self.surface, self.pos)

def add_alphabet_line(alphabet_string):
    y = screen_height // 4  # 상단에 위치시키기 위해 화면 높이의 1/4 지점에 배치
    line = []
    x = (screen_width - len(alphabet_string) * 40) // 2  # 중간 정렬
    for char in alphabet_string:
        line.append(Alphabet(char, x, y))
        x += 40  # 각 알파벳의 간격을 조정합니다
    falling_lines.append(line)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and alphabet_line:
                add_alphabet_line(''.join(alphabet_line))
                alphabet_line = []
            elif event.key == pygame.K_BACKSPACE and alphabet_line:
                alphabet_line.pop()
            elif event.unicode.isalpha():
                alphabet_line.append(event.unicode.upper())

    # 업데이트
    for line in falling_lines:
        for alphabet in line:
            alphabet.update()

    # 화면 그리기
    screen.fill(black)
    
    # 입력된 알파벳 한 줄 그리기
    x = (screen_width - len(alphabet_line) * 40) // 2
    y = screen_height // 4
    for char in alphabet_line:
        text = font.render(char, True, white)
        screen.blit(text, (x, y))
        x += 40

    # 떨어지는 알파벳 그리기
    for line in falling_lines:
        for alphabet in line:
            alphabet.draw(screen)

    # 장애물 그리기
    for obstacle in obstacles:
        pygame.draw.rect(screen, red, obstacle)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()

