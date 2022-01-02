import pygame
import random


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def load_field():
    with open("field.txt", mode="r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace("\n", "")
            line = line.split()
            cell = Cell(int(line[0]), int(line[1]), line[2])
            all_sprites.add(cell)


class Dice(pygame.sprite.Sprite):
    values = {1: "dice1",
              2: "dice2",
              3: "dice3",
              4: "dice4",
              5: "dice5",
              6: "dice6"}

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("dice1.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def change_image(self):
        self.image = pygame.image.load(f"dice{random.randint(1, 6)}.png")


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((700, 600))

    all_sprites = pygame.sprite.Group()

    load_field()

    dice1 = Dice(350, 450)
    dice2 = Dice(500, 450)
    all_sprites.add(dice1)
    all_sprites.add(dice2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                dice1.change_image()
                dice2.change_image()

        screen.fill("black")
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()