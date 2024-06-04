import pygame
import math

class Mario:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load("picture/mario.png")
        self.image = pygame.transform.scale(self.image, (60, 100))
        self.rect = self.image.get_rect()
        self.speed = 30
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.start_pos = [screen_width // 2 - 50, screen_height - 200]
        self.reset()
        self.count = 0

    def reset(self):
        self.x, self.y = self.start_pos
        self.vx, self.vy = 0, 0
        self.grabbed = False

    def update(self, obstacles, hidden_alphabets, block_hit_sound, falling_lines):
        if not self.grabbed:
            norm = math.hypot(self.vx, self.vy)
            if norm != 0:
                self.x += self.speed * self.vx / norm
                self.y += self.speed * self.vy / norm

            self.rect.topleft = (self.x, self.y)
            for i, obstacle in enumerate(obstacles):
                if self.rect.colliderect(obstacle):
                    block_hit_sound.play()  # 블록 히트 사운드 재생
                    falling_lines.append([hidden_alphabets[i]])
                    hidden_alphabets[i].velocity = [0, 5]
                    hidden_alphabets.pop(i)
                    obstacles.pop(i)
                    self.reset()
                    break

            if self.x < 0 or self.x > self.screen_width or self.y < 0 or self.y > self.screen_height:
                self.reset()

