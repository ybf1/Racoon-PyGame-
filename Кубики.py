import pygame
import os
import sys
import random


nums = {1: 'Кубик 1',
        2: 'Кубик 2',
        3: 'Кубик 3',
        4: 'Кубик 4',
        5: 'Кубик 5',
        6: 'Кубик 6'}


image = pygame.Surface([100, 100])
image.fill(pygame.Color("black"))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


if __name__ == '__main__':
    running = True
    while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    image1 = load_image(nums[random.choice(range(1, 7))])
                    image2 = load_image(nums[random.choice(range(1, 7))])



