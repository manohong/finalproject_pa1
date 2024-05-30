import pygame
import random
import sys
import math

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
small_font = pygame.font.Font(None, 36)

# 단어 리스트 설정
words = ["PYTHON", "JAZZ", "APPLE", "BANANA", "CHERRY", "ORANGE", "GRAPE", "LEMON", "LIME", "KIWI", "MANGO", "PEACH", "PIG", "DATE", "OLIVE", "TOMATO", "CARROT"]
current_word = random.choice(words)

# 알파벳 줄 설정
alphabet_line = []
falling_lines = []

# 장애물 설정
obstacles = []
for _ in range(len(current_word)):
    x = random.randint(0, screen_width - 50)
    y = random.randint(50, screen_height // 3)  # 장애물을 화면 상단에 배치
    obstacles.append(pygame.Rect(x, y, 50, 50))

# 공 설정
ball_radius = 10
ball_speed = 15
ball_start_pos = [screen_width // 2, screen_height - 60]  # 공의 초기 위치를 약간 위로 설정
ball = None
ball_grabbed = False
ball_count = 0  # 사용한 공의 횟수

# 게임 루프
clock = pygame.time.Clock()
running = True
game_over = False

class Alphabet:
    def __init__(self, char, x, y):
        self.char = char
        self.pos = [x, y]
        self.velocity = [0, 5]
        self.surface = font.render(char, True, white)
        self.grounded = False

    def update(self):
        if not self.grounded:
            self.pos[1] += self.velocity[1]

        alphabet_rect = pygame.Rect(self.pos[0], self.pos[1], self.surface.get_width(), self.surface.get_height())

        for obstacle in obstacles:
            if alphabet_rect.colliderect(obstacle):
                self.grounded = True
                if alphabet_rect.bottom > obstacle.top and alphabet_rect.top < obstacle.top:
                    self.pos[1] = obstacle.top - self.surface.get_height()
                    break

        if self.pos[1] >= screen_height - self.surface.get_height():
            self.pos[1] = screen_height - self.surface.get_height()
            self.grounded = True

    def draw(self, screen):
        screen.blit(self.surface, self.pos)

def hide_alphabets_behind_obstacles(word):
    hidden_alphabets = []
    for i, char in enumerate(word):
        x, y = obstacles[i].center
        hidden_alphabets.append(Alphabet(char, x, y))
    return hidden_alphabets

hidden_alphabets = hide_alphabets_behind_obstacles(current_word)

def add_alphabet_line(alphabet_string):
    y = screen_height - 150  # 입력된 알파벳 줄을 화면 하단에서 약간 위로 배치
    line = []
    x = (screen_width - len(alphabet_string) * 40) // 2
    for char in alphabet_string:
        line.append(Alphabet(char, x, y))
        x += 40
    falling_lines.append(line)

def create_ball():
    return [ball_start_pos[0], ball_start_pos[1], 0, 0]

ball = create_ball()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = event.pos
            if ball and not ball_grabbed and math.hypot(mouse_pos[0] - ball[0], mouse_pos[1] - ball[1]) <= ball_radius:
                ball_grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP and ball_grabbed:
            ball_grabbed = False
            mouse_pos = event.pos
            ball[2] = ball[0] - mouse_pos[0]
            ball[3] = ball[1] - mouse_pos[1]
            ball_count += 1  # 공을 쏠 때마다 카운트 증가
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and alphabet_line:
                entered_word = ''.join(alphabet_line)
                if entered_word == current_word:
                    game_over = True
                else:
                    alphabet_line = []
            elif event.key == pygame.K_BACKSPACE and alphabet_line:
                alphabet_line.pop()
            elif event.unicode.isalpha() and not game_over:
                alphabet_line.append(event.unicode.upper())

    if ball and not ball_grabbed:
        norm = math.hypot(ball[2], ball[3])
        if norm != 0:
            ball[0] += ball_speed * ball[2] / norm
            ball[1] += ball_speed * ball[3] / norm

        ball_rect = pygame.Rect(ball[0] - ball_radius, ball[1] - ball_radius, ball_radius * 2, ball_radius * 2)
        for i, obstacle in enumerate(obstacles):
            if ball_rect.colliderect(obstacle):
                falling_lines.append([hidden_alphabets[i]])
                hidden_alphabets[i].velocity = [0, 5]
                hidden_alphabets.pop(i)
                obstacles.pop(i)
                ball = None
                break

        if ball and (ball[0] < 0 or ball[0] > screen_width or ball[1] < 0 or ball[1] > screen_height):
            ball = None

    if not ball:
        ball = create_ball()

    for line in falling_lines:
        for alphabet in line:
            alphabet.update()

    screen.fill(black)

    x = (screen_width - len(alphabet_line) * 40) // 2
    y = screen_height - 150  # 입력된 알파벳 줄 위치 조정
    for char in alphabet_line:
        text = font.render(char, True, white)
        screen.blit(text, (x, y))
        x += 40

    for line in falling_lines:
        for alphabet in line:
            alphabet.draw(screen)

    for obstacle in obstacles:
        pygame.draw.rect(screen, red, obstacle)

    if ball:
        pygame.draw.circle(screen, white, (int(ball[0]), int(ball[1])), ball_radius)
        if ball_grabbed:
            pygame.draw.line(screen, white, (ball[0], ball[1]), pygame.mouse.get_pos())

    ball_count_text = small_font.render(f"Balls Used: {ball_count}", True, white)
    screen.blit(ball_count_text, (10, 10))

    if game_over:
        game_over_text = font.render("YOU WIN!", True, white)
        screen.blit(game_over_text, ((screen_width - game_over_text.get_width()) // 2, screen_height // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()

