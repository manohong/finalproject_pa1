import pygame
import random

def create_obstacles(word_length, block_size, screen_width, screen_height):
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

