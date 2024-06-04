import pygame

class Alphabet:
    def __init__(self, char, x, y):
        self.char = char
        self.pos = [x, y]
        self.velocity = [0, 5]
        self.surface = pygame.font.Font(None, 74).render(char, True, (0, 0, 0))
        self.grounded = False

    def update(self, obstacles, screen_height):
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

def hide_alphabets_behind_obstacles(word, obstacles):
    hidden_alphabets = []
    for i, char in enumerate(word):
        x, y = obstacles[i].center
        hidden_alphabets.append(Alphabet(char, x, y))
    return hidden_alphabets

def add_alphabet_line(alphabet_string, falling_lines, screen_width, screen_height):
    y = screen_height - 150  # 입력된 알파벳 줄을 화면 하단에서 약간 위로 배치
    line = []
    x = (screen_width - len(alphabet_string) * 40) // 2
    for char in alphabet_string:
        line.append(Alphabet(char, x, y))
        x += 40
    falling_lines.append(line)

