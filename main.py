import pygame
import random
import sys
import os


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, color, number):
        super().__init__()
        self.number = number
        self.is_free = True
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
            cell = Cell(int(line[0]), int(line[1]), line[2], float(line[3]))
            cells.append(cell)
            all_sprites.add(cell)


class Dice(pygame.sprite.Sprite):
    values = {1: "dice1",
              2: "dice2",
              3: "dice3",
              4: "dice4",
              5: "dice5",
              6: "dice6"}

    def __init__(self, x, y, num):
        super().__init__()
        self.image = pygame.image.load("dice1.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.num = num

    def change_image(self):
        res = random.randint(1, 6)
        dice_values[self.num] = res
        self.image = pygame.image.load(f"dice{res}.png")


class Chip(pygame.sprite.Sprite):
    def __init__(self, player, cell_number):
        super().__init__()
        self.player = player
        self.cell_number = cell_number
        self.image = pygame.Surface((20, 20))
        self.image.fill(player)
        self.rect = self.image.get_rect()


class Menu:
    def __init__(self, items=[400, 350, 'Item', (250, 250, 30), (250, 30, 250)]):
        self.items = items

    def render(self, surface, font, num_item):
        for i in self.items:
            if num_item == i[5]:
                surface.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30))
            else:
                surface.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30))

    def menu(self):
        running = True
        font_menu = pygame.font.Font(None, 50)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        item = 0
        while running:
            info.fill((0, 100, 200))
            screen.fill((0, 100, 200))

            mp = pygame.mouse.get_pos()
            for i in self.items:
                if (mp[0] > i[0]) and (mp[0] < i[0] + 155) and (mp[1] > i[1]) and (mp[1] < i[1] + 50):
                    item = i[5]
            self.render(screen, font_menu, item)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_UP:
                        if item > 0:
                            item -= 1
                    if event.key == pygame.K_DOWN:
                        if item < len(self.items) - 1:
                            item += 1
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if item == 0:
                        running = False
                        pygame.mixer.music.unpause()
                    elif item == 1:
                        exit()
            screen.blit(info, (0, 0))
            screen.blit(screen, (0, 30))
            pygame.display.flip()


def is_free_red():
    for cell in cells:
        if cell.number == 1 and cell.is_free:
            cell.is_free = False #вот эту строчку в отдельную функцию
            return True
    return False


def is_free_green():
    for cell in cells:
        if cell.number == 43 and cell.is_free:
            cell.is_free = False #вот эту строчку в отдельную функцию
            return True
    return False


def is_free_blue():
    for cell in cells:
        if cell.number == 29 and cell.is_free:
            cell.is_free = False #вот эту строчку в отдельную функцию
            return True
    return False


def is_free_yellow():
    for cell in cells:
        if cell.number == 15 and cell.is_free:
            cell.is_free = False #вот эту строчку в отдельную функцию
            return True
    return False


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((700, 600))
    info = pygame.Surface((800, 30))
    items = [(350, 300, 'Play', (11, 0, 77), (250, 250, 30), 0),
              (350, 340, 'Exit', (11, 0, 77), (250, 250, 30), 1)]
    game = Menu(items)
    game.menu()
    WIDTH, HEIGHT = 700, 600
    FPS = 60
    clock = pygame.time.Clock()
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(loops=-1)

    all_sprites = pygame.sprite.Group()
    cells = []
    chips = []

    load_field()
    cell1 = cells[0]
    print(cell1)

    dice1 = Dice(350, 450, 0)
    dice2 = Dice(500, 450, 1)
    all_sprites.add(dice1)
    all_sprites.add(dice2)
    dice_values = [0, 0]

    current_player = -1
    players_chips = {"red": 0,
                     "green": 0,
                     "blue": 0,
                     "yellow": 0}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                dice1.change_image()
                dice2.change_image()
                current_player = (current_player + 1) % 4
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.pause()
                game.menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for chip in chips:
                        if chip.rect.collidepoint(event.pos):
                            if dice_values[0]:
                                for cell in cells:
                                    if cell.number == chip.cell_number:
                                        cell.is_free = True
                                chip.cell_number += dice_values[0]
                                for cell in cells:
                                    if cell.number == chip.cell_number:
                                        cell.is_free = False
                                dice_values[0] = 0
                            else:
                                for cell in cells:
                                    if cell.number == chip.cell_number:
                                        cell.is_free = True
                                chip.cell_number += dice_values[1]
                                for cell in cells:
                                    if cell.number == chip.cell_number:
                                        cell.is_free = False
                                dice_values[1] = 0
                if event.button == 3:
                    for cell in cells:
                        if cell.rect.collidepoint(event.pos) and cell.number == 1.1:
                            if current_player == 0 and players_chips["red"] <= 5:
                                if is_free_red():
                                    print(1)
                                    if dice_values[0]:
                                        chip = Chip("pink", 1)
                                        all_sprites.add(chip)
                                        chips.append(chip)
                                        dice_values[0] = 0
                                        players_chips["red"] += 1
                                    elif dice_values[1]:
                                        chip = Chip("pink", 1)
                                        all_sprites.add(chip)
                                        chips.append(chip)
                                        dice_values[1] = 0
                                        players_chips["red"] += 1
                        if cell.rect.collidepoint(event.pos) and cell.number == 43.1:
                            if current_player == 1 and players_chips["green"] <= 5:
                                if is_free_green():
                                    print(1)
                                    if dice_values[0]:
                                        chip = Chip("green", 43)
                                        all_sprites.add(chip)
                                        chips.append(chip)
                                        dice_values[0] = 0
                                        players_chips["green"] += 1
                                    elif dice_values[1]:
                                        chip = Chip("green", 43)
                                        all_sprites.add(chip)
                                        chips.append(chip)
                                        dice_values[1] = 0
                                        players_chips["green"] += 1
                        if cell.rect.collidepoint(event.pos) and cell.number == 29.1:
                            if current_player == 2 and players_chips["blue"] <= 5:
                                if is_free_blue():
                                    print(1)
                                    if dice_values[0]:
                                        chip = Chip("blue", 29)
                                        all_sprites.add(chip)
                                        chips.append(chip)
                                        dice_values[0] = 0
                                        players_chips["blue"] += 1
                                    elif dice_values[1]:
                                        chip = Chip("blue", 29)
                                        all_sprites.add(chip)
                                        chips.append(chip)
                                        dice_values[1] = 0
                                        players_chips["blue"] += 1
                        if cell.rect.collidepoint(event.pos) and cell.number == 15.1:
                            if current_player == 3 and players_chips["yellow"] <= 5:
                                if is_free_yellow():
                                    print(1)
                                    if dice_values[0]:
                                        chip = Chip("yellow", 15)
                                        all_sprites.add(chip)
                                        chips.append(chip)
                                        dice_values[0] = 0
                                        players_chips["yellow"] += 1
                                    elif dice_values[1]:
                                        chip = Chip("yellow", 15)
                                        all_sprites.add(chip)
                                        chips.append(chip)
                                        dice_values[1] = 0
                                        players_chips["yellow"] += 1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                pygame.mixer.music.pause()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                pygame.mixer.music.unpause()
                pygame.mixer.music.set_volume(0.5)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                pygame.mixer.music.unpause()
                pygame.mixer.music.set_volume(1)

        for chip in chips:
            for cell in cells:
                if cell.number == chip.cell_number:
                    chip.rect.x = cell.rect.x + 5
                    chip.rect.y = cell.rect.y + 5

        screen.fill("black")
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()