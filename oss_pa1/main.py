import pygame
import sys
from game import FallingAlphabetGame

# 초기 설정
pygame.init()
pygame.mixer.init()  # 사운드 초기화

# 화면 크기 설정
screen_width = 1366
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Falling Alphabet Game")

# 사운드 로드
block_hit_sound = pygame.mixer.Sound("sound/blockhit.wav")
game_over_sound = pygame.mixer.Sound("sound/gameover.wav")
background_music = "sound/overworld-fast.wav"

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

# 게임 인스턴스 생성
sounds = {
    "block_hit": block_hit_sound,
    "game_over": game_over_sound
}

game = FallingAlphabetGame(screen_width, screen_height, words, "picture/block.png", "picture/map.png", sounds)
game.load_assets()

# 게임 루프
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if not game.handle_event(event):
            running = False

    game.update()
    game.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()

