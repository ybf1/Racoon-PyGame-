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
    pygame.init()
    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)
    cubes_sprites = pygame.sprite.Group()
    sprite1 = pygame.sprite.Sprite()
    sprite2 = pygame.sprite.Sprite()
    cubes_sprites.add(sprite1)
    cubes_sprites.add(sprite2)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                screen.fill(pygame.Color('white'))
                sprite1.image = load_image(nums[random.choice(range(1, 7))] + '.png')
                sprite1.rect = sprite1.image.get_rect()
                sprite2.image = load_image(nums[random.choice(range(1, 7))] + '.png')
                sprite2.rect = sprite2.image.get_rect()
                sprite1.rect.x = 5
                sprite1.rect.y = 20
                sprite2.rect.x = 5 + 40
                sprite2.rect.y = 20
                cubes_sprites.draw(screen)
            pygame.display.flip()
        pygame.quit()



