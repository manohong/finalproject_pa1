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

# 단어 리스트 설정
words = ["PYTHON", "JAZZ", "APPLE", "BANANA", "CHERRY"]
current_word = random.choice(words)

# 알파벳 줄 설정
alphabet_line = []
falling_lines = []

# 장애물 설정
obstacles = []
for _ in range(len(current_word)):
    x = random.randint(0, screen_width - 50)
    y = random.randint(screen_height // 2, screen_height - 50)
    obstacles.append(pygame.Rect(x, y, 50, 50))

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
    y = screen_height // 4
    line = []
    x = (screen_width - len(alphabet_string) * 40) // 2
    for char in alphabet_string:
        line.append(Alphabet(char, x, y))
        x += 40
    falling_lines.append(line)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = event.pos
            for i, obstacle in enumerate(obstacles):
                if obstacle.collidepoint(mouse_pos):
                    falling_lines.append([hidden_alphabets[i]])
                    hidden_alphabets[i].velocity = [0, 5]
                    hidden_alphabets.pop(i)
                    obstacles.pop(i)
                    break
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

    for line in falling_lines:
        for alphabet in line:
            alphabet.update()

    screen.fill(black)
    
    x = (screen_width - len(alphabet_line) * 40) // 2
    y = screen_height // 4
    for char in alphabet_line:
        text = font.render(char, True, white)
        screen.blit(text, (x, y))
        x += 40

    for line in falling_lines:
        for alphabet in line:
            alphabet.draw(screen)

    for obstacle in obstacles:
        pygame.draw.rect(screen, red, obstacle)

    if game_over:
        game_over_text = font.render("YOU WIN!", True, white)
        screen.blit(game_over_text, ((screen_width - game_over_text.get_width()) // 2, screen_height // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()

