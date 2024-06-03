import pygame
import random
import sys
import math
import time

pygame.init()
pygame.mixer.init()  # 사운드 초기화

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Falling Alphabet Game")

# 색상 설정
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
sky_blue = (135, 206, 235)

# 폰트 설정
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# 사운드 로드
block_hit_sound = pygame.mixer.Sound("blockhit.wav")
game_over_sound = pygame.mixer.Sound("gameover.wav")
background_music = "overworld-fast.wav"

# 배경 음악 설정 및 재생
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  # 무한 반복 재생

# 단어 리스트 설정
words = ["PYTHON", "JAZZ", "APPLE", "BANANA", "CHERRY", "ORANGE", "GRAPE", "LEMON", "LIME", "KIWI", "MANGO",
         "PEACH", "PIG", "DATE", "OLIVE", "TOMATO", "CARROT", "DOG", "CAT", "COW", "HEN", "GOAT", "SHEEP",
         "DUCK", "FISH", "BIRD", "BEE", "ANT", "BELL", "BOOK", "BOOT", "BALL", "BAG", "CUP", "CANE", "COIN",
         "DEER", "DICE", "DOLL", "DRUM", "FLAG", "FORK", "FROG", "GATE", "GIFT", "HAT", "HUT", "INK", "JAR",
         "KITE", "LAMP", "MAP", "MOON", "NET", "OWL", "PEN", "POT", "ROSE", "SUN", "TENT", "TOY", "VAN", "WALL",
         "WAX", "YARN", "ZEBRA"]

current_word = random.choice(words)

# 알파벳 줄 설정
alphabet_line = []
falling_lines = []

# 장애물 이미지 로드 및 크기 설정
block_image = pygame.image.load("block.png")
block_size = (int(block_image.get_width() * 0.7), int(block_image.get_height() * 0.7))
block_image = pygame.transform.scale(block_image, block_size)

# 배경 이미지 로드 및 크기 설정
map_image = pygame.image.load("map.png")
map_image = pygame.transform.scale(map_image, (screen_width, map_image.get_height() // 3))

# 장애물 설정
def create_obstacles(word_length, block_size):
    obstacles = []
    while len(obstacles) < word_length:
        x = random.randint(0, screen_width - block_size[0])
        y = random.randint(50, screen_height // 3)
        new_obstacle = pygame.Rect(x, y, *block_size)
        
        # Check for overlap
        overlap = False
        for obstacle in obstacles:
            if new_obstacle.colliderect(obstacle):
                overlap = True
                break
        
        if not overlap:
            obstacles.append(new_obstacle)
    
    return obstacles

obstacles = create_obstacles(len(current_word), block_size)

# 마리오 이미지 설정
mario_image = pygame.image.load("mario.png")
mario_image = pygame.transform.scale(mario_image, (60, 60)) 
mario_rect = mario_image.get_rect()
mario_speed = 30
mario_start_pos = [screen_width // 2 -50, screen_height - 100]  # 마리오의 초기 위치를 약간 위로 설정
mario = None
mario_grabbed = False
mario_count = 0  # 사용한 마리오의 횟수

# 게임 타이머 초기화
start_time = time.time()
timer_paused = False
end_time = 0

# 게임 루프
clock = pygame.time.Clock()
running = True
game_over = False

class Alphabet:
    def __init__(self, char, x, y):
        self.char = char
        self.pos = [x, y]
        self.velocity = [0, 5]
        self.surface = font.render(char, True, black)
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

def create_mario():
    return [mario_start_pos[0], mario_start_pos[1], 0, 0]

mario = create_mario()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = event.pos
            mario_center = [mario[0] + mario_rect.width // 2, mario[1] + mario_rect.height // 2]
            if mario and not mario_grabbed and math.hypot(mouse_pos[0] - mario_center[0], mouse_pos[1] - mario_center[1]) <= mario_rect.width // 2:
                mario_grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP and mario_grabbed:
            mario_grabbed = False
            mouse_pos = event.pos
            mario[2] = mario_center[0] - mouse_pos[0]  # 반대로 당긴 방향으로 발사
            mario[3] = mario_center[1] - mouse_pos[1]  # 반대로 당긴 방향으로 발사
            mario_count += 1  # 마리오를 쏠 때마다 카운트 증가
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and alphabet_line:
                entered_word = ''.join(alphabet_line)
                if entered_word == current_word:
                    game_over = True
                    alphabet_line = []  # game_over가 되었을 때 입력한 단어 지우기
                    timer_paused = True  # 타이머 정지
                    end_time = time.time() - start_time
                    pygame.mixer.music.stop()  # 배경 음악 중지
                    game_over_sound.play()  # 게임 오버 사운드 재생
                else:
                    alphabet_line = []
            elif event.key == pygame.K_BACKSPACE and alphabet_line:
                alphabet_line.pop()
            elif event.unicode.isalpha() and not game_over:
                alphabet_line.append(event.unicode.upper())

    if mario and not mario_grabbed:
        norm = math.hypot(mario[2], mario[3])
        if norm != 0:
            mario[0] += mario_speed * mario[2] / norm
            mario[1] += mario_speed * mario[3] / norm

        mario_rect.topleft = (mario[0], mario[1])
        for i, obstacle in enumerate(obstacles):
            if mario_rect.colliderect(obstacle):
                block_hit_sound.play()  # 블록 히트 사운드 재생
                falling_lines.append([hidden_alphabets[i]])
                hidden_alphabets[i].velocity = [0, 5]
                hidden_alphabets.pop(i)
                obstacles.pop(i)
                mario = None
                break

        if mario and (mario[0] < 0 or mario[0] > screen_width or mario[1] < 0 or mario[1] > screen_height):
            mario = None

    if not mario:
        mario = create_mario()

    for line in falling_lines:
        for alphabet in line:
            alphabet.update()

    screen.fill(sky_blue)  # 배경 색상을 하늘색으로 설정

    # 배경 이미지 그리기 (하단에만 위치)
    screen.blit(map_image, (0, screen_height - map_image.get_height()))

    x = (screen_width - len(alphabet_line) * 40) // 2
    y = screen_height - 300  # 입력된 알파벳 줄 위치 조정
    for char in alphabet_line:
        text = font.render(char, True, black)
        screen.blit(text, (x, y))
        x += 40

    for line in falling_lines:
        for alphabet in line:
            alphabet.draw(screen)

    for obstacle in obstacles:
        screen.blit(block_image, obstacle.topleft)

    if mario:
        screen.blit(mario_image, mario_rect.topleft)
        if mario_grabbed:
            pygame.draw.line(screen, white, (mario_center[0], mario_center[1]), pygame.mouse.get_pos())

    mario_count_text = small_font.render(f"Marios Used: {mario_count}", True, white)
    mario_count_rect = mario_count_text.get_rect()
    mario_count_rect.topleft = (10, 10)
    pygame.draw.rect(screen, black, mario_count_rect.inflate(10, 10))
    screen.blit(mario_count_text, (10, 10))

    # 타이머 표시
    if not timer_paused:
        elapsed_time = time.time() - start_time
    else:
        elapsed_time = end_time
    timer_text = small_font.render(f"Time: {elapsed_time:.2f}s", True, white)
    screen.blit(timer_text, (screen_width - 150, 10))

    if game_over:
        end_time = elapsed_time  # 타이머 정지 후 시간을 저장
        game_over_text = small_font.render(f"YOU WIN! Time: {end_time:.2f}s Marios Used: {mario_count}", True, white)
        screen.blit(game_over_text, ((screen_width - game_over_text.get_width()) // 2, screen_height // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()

