import pygame
import random
import math
from mario import Mario
from alphabet import Alphabet, hide_alphabets_behind_obstacles, add_alphabet_line
from timer import Timer
from obstacles import create_obstacles

class FallingAlphabetGame:
    def __init__(self, screen_width, screen_height, words, block_image_path, map_image_path, sounds):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.words = words
        self.block_image_path = block_image_path
        self.map_image_path = map_image_path
        self.sounds = sounds
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 50)
        self.load_assets()
        self.reset_game()

    def reset_game(self):
        self.current_word = random.choice(self.words)
        self.obstacles = create_obstacles(len(self.current_word), self.block_size, self.screen_width, self.screen_height)
        self.hidden_alphabets = hide_alphabets_behind_obstacles(self.current_word, self.obstacles)
        self.alphabet_line = []
        self.falling_lines = []
        self.mario = Mario(self.screen_width, self.screen_height)
        self.mario_count = 0
        self.game_over = False
        self.timer = Timer()
        self.timer.start()
        pygame.mixer.music.play(-1)  # 배경 음악 재생

    def load_assets(self):
        self.block_image = pygame.image.load(self.block_image_path)
        self.block_size = (int(self.block_image.get_width() * 0.7), int(self.block_image.get_height() * 0.7))
        self.block_image = pygame.transform.scale(self.block_image, self.block_size)
        self.map_image = pygame.image.load(self.map_image_path)
        self.map_image = pygame.transform.scale(self.map_image, (self.screen_width, self.map_image.get_height() // 3))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            mouse_pos = event.pos
            mario_center = [self.mario.x + self.mario.rect.width // 2, self.mario.y + self.mario.rect.height // 2]
            if not self.mario.grabbed and math.hypot(mouse_pos[0] - mario_center[0], mouse_pos[1] - mario_center[1]) <= self.mario.rect.width // 2:
                self.mario.grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP and self.mario.grabbed:
            self.mario.grabbed = False
            mouse_pos = event.pos
            mario_center = [self.mario.x + self.mario.rect.width // 2, self.mario.y + self.mario.rect.height // 2]
            self.mario.vx = mario_center[0] - mouse_pos[0]  # 반대로 당긴 방향으로 발사
            self.mario.vy = mario_center[1] - mouse_pos[1]  # 반대로 당긴 방향으로 발사
            self.mario.count += 1  # 마리오를 쏠 때마다 카운트 증가
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.alphabet_line:
                entered_word = ''.join(self.alphabet_line)
                if entered_word == self.current_word:
                    self.game_over = True
                    self.alphabet_line = []  # game_over가 되었을 때 입력한 단어 지우기
                    self.timer.pause()  # 타이머 정지
                    pygame.mixer.music.stop()  # 배경 음악 중지
                    self.sounds["game_over"].play()  # 게임 오버 사운드 재생
                else:
                    self.alphabet_line = []
            elif event.key == pygame.K_BACKSPACE and self.alphabet_line:
                self.alphabet_line.pop()
            elif event.unicode.isalpha() and not self.game_over:
                self.alphabet_line.append(event.unicode.upper())
        elif event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
            if self.retry_button.collidepoint(event.pos):
                self.reset_game()
        return True

    def update(self):
        self.mario.update(self.obstacles, self.hidden_alphabets, self.sounds["block_hit"], self.falling_lines)

    def draw(self, screen):
        screen.fill((135, 206, 235))  # 배경 색상을 하늘색으로 설정

        # 배경 이미지 그리기 (하단에만 위치)
        screen.blit(self.map_image, (0, self.screen_height - self.map_image.get_height()))

        x = (self.screen_width - len(self.alphabet_line) * 40) // 2
        y = self.screen_height - 300  # 입력된 알파벳 줄 위치 조정
        for char in self.alphabet_line:
            text = self.font.render(char, True, (0, 0, 0))
            screen.blit(text, (x, y))
            x += 40

        for line in self.falling_lines:
            for alphabet in line:
                alphabet.update(self.obstacles, self.screen_height)
                alphabet.draw(screen)

        for obstacle in self.obstacles:
            screen.blit(self.block_image, obstacle.topleft)

        if self.mario:
            screen.blit(self.mario.image, self.mario.rect.topleft)
            if self.mario.grabbed:
                pygame.draw.line(screen, (255, 255, 255), (self.mario.x + self.mario.rect.width // 2, self.mario.y + self.mario.rect.height // 2), pygame.mouse.get_pos())

        mario_count_text = self.small_font.render(f"Marios Used: {self.mario.count}", True, (255, 255, 255))
        mario_count_rect = mario_count_text.get_rect()
        mario_count_rect.topleft = (10, 10)
        pygame.draw.rect(screen, (0, 0, 0), mario_count_rect.inflate(10, 10))
        screen.blit(mario_count_text, (10, 10))

        # 타이머 표시
        elapsed_time = self.timer.get_elapsed_time()
        timer_text = self.small_font.render(f"Time: {elapsed_time:.2f}s", True, (255, 255, 255))
        screen.blit(timer_text, (self.screen_width - 220, 10))

        if self.game_over:
            game_over_text = self.small_font.render(f"YOU WIN! Time: {elapsed_time:.2f}s Marios Used: {self.mario.count}", True, (255, 255, 255))
            screen.blit(game_over_text, ((self.screen_width - game_over_text.get_width()) // 2, self.screen_height // 2))
            
            self.retry_button = pygame.Rect((self.screen_width - 200) // 2, self.screen_height // 2 + 50, 200, 50)
            pygame.draw.rect(screen, (0, 0, 0), self.retry_button)
            retry_text = self.small_font.render("Retry", True, (255, 255, 255))
            retry_text_rect = retry_text.get_rect(center=self.retry_button.center)
            screen.blit(retry_text, retry_text_rect)

