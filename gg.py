import pygame
import random
import sys
import os
import time


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, color, number):
        super().__init__()
        self.number = number
        self.is_free = True
        self.image = pygame.image.load(f"{color}.png")
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
        self.count = 1
        self.on_finish = False


class FinalScreen:
    def __init__(self, items=[400, 350, 'Item', (250, 250, 30), (250, 30, 250)]):
        self.items = items

    def render(self, surface, font, num_item):
        for i in self.items:
            if num_item == i[5]:
                surface.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30))
            else:
                surface.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30))

    def finscreen(self):
        running = True
        font_menu = pygame.font.Font(None, 50)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        item = 0
        while running:
            info.fill((0, 100, 200))
            screen.fill((0, 100, 200))
            self.render(screen, font_menu, item)
            screen.blit(info, (0, 0))
            screen.blit(screen, (0, 30))
            pygame.display.flip()
            pygame.mixer.music.pause()
            create_particles((random.randint(1, 700), random.randint(1, 600)))
            create_particles((random.randint(1, 700), random.randint(1, 600)))
            create_particles((random.randint(1, 700), random.randint(1, 600)))
            create_particles((random.randint(1, 700), random.randint(1, 600)))
            create_particles((random.randint(1, 700), random.randint(1, 600)))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


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


def make_false(num):
    for cell in cells:
        if cell.number == num:
            cell.is_free = False


def is_free(num):
    for cell in cells:
        if cell.number == num and cell.is_free:
            return True
    return False


if __name__ == '__main__':
    pygame.init()
    GRAVITY = 0.5
    screen = pygame.display.set_mode((700, 600))
    info = pygame.Surface((800, 30))
    items = [(305, 280, 'Play', (11, 0, 77), (250, 250, 30), 0),
             (305, 320, 'Exit', (11, 0, 77), (250, 250, 30), 1)]
    game = Menu(items)
    game.menu()
    final_text = [(250, 250, 'Game over', (11, 0, 77), (250, 250, 30), 0),
                  (165, 300, 'WINNER', (11, 0, 77), (250, 250, 30), 1)]
    final = FinalScreen(final_text)
    WIDTH, HEIGHT = 700, 600
    screen_rect = (0, 0, WIDTH, HEIGHT)
    FPS = 60
    clock = pygame.time.Clock()
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(loops=-1)

    all_sprites = pygame.sprite.Group()
    cells = []
    chips = []
    red_chips = []
    green_chips = []
    blue_chips = []
    yellow_chips = []
    chips_groups = {0: red_chips, 1: green_chips, 2: blue_chips, 3: yellow_chips}

    load_field()

    dice1 = Dice(350, 450, 0)
    dice2 = Dice(500, 450, 1)
    all_sprites.add(dice1)
    all_sprites.add(dice2)
    dice_values = [0, 0]

    current_player = -1
    players = ["pink", "green", "blue", "yellow"]
    players_chips = {"pink": [0, 1],
                     "green": [0, 5],
                     "blue": [0, 5],
                     "yellow": [0, 5]}

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
                        if chip.rect.collidepoint(event.pos) and chip.player == players[current_player]:
                            if dice_values[0]:
                                for cell in cells:
                                    if cell.number == chip.cell_number + dice_values[0] and cell.is_free:
                                        can_move = True
                                    elif cell.number == chip.cell_number + dice_values[0] and not cell.is_free:
                                        can_move = False
                                        n = cell.number

                                if can_move:
                                    for cell in cells:
                                        if cell.number == chip.cell_number:
                                            cell.is_free = True
                                    chip.cell_number += dice_values[0]
                                    chip.count += dice_values[0]
                                    for cell in cells:
                                        if cell.number == chip.cell_number:
                                            cell.is_free = False
                                    dice_values[0] = 0
                                else:
                                    for chip1 in chips:
                                        if chip1.cell_number == n and chip1.player == chip.player:
                                            can_eat = False
                                        elif chip1.cell_number == n and chip1.player != chip.player:
                                            can_eat = True
                                    if can_eat:
                                        for chip1 in chips:
                                            if chip1.cell_number == n:
                                                chip1.kill()
                                                players_chips[chip1.player][0] -= 1
                                        for cell in cells:
                                            if cell.number == chip.cell_number:
                                                cell.is_free = True
                                        chip.cell_number += dice_values[0]
                                        chip.count += dice_values[0]
                                        for cell in cells:
                                            if cell.number == chip.cell_number:
                                                cell.is_free = False
                                        dice_values[0] = 0
                            else:
                                for cell in cells:
                                    if cell.number == chip.cell_number + dice_values[1] and cell.is_free:
                                        can_move = True
                                    elif cell.number == chip.cell_number + dice_values[1] and not cell.is_free:
                                        can_move = False
                                        n = cell.number

                                if can_move:
                                    for cell in cells:
                                        if cell.number == chip.cell_number:
                                            cell.is_free = True
                                    chip.cell_number += dice_values[1]
                                    chip.count += dice_values[1]
                                    for cell in cells:
                                        if cell.number == chip.cell_number:
                                            cell.is_free = False
                                    dice_values[1] = 0
                                else:
                                    for chip1 in chips:
                                        if chip1.cell_number == n and chip1.player == chip.player:
                                            can_eat = False
                                        elif chip1.cell_number == n and chip1.player != chip.player:
                                            can_eat = True
                                    if can_eat:
                                        for chip1 in chips:
                                            if chip1.cell_number == n:
                                                chip1.kill()
                                                players_chips[chip1.player] -= 1
                                        for cell in cells:
                                            if cell.number == chip.cell_number:
                                                cell.is_free = True
                                        chip.cell_number += dice_values[1]
                                        chip.count += dice_values[1]
                                        for cell in cells:
                                            if cell.number == chip.cell_number:
                                                cell.is_free = False
                                        dice_values[1] = 0
                    for chip in chips:
                        if chip.cell_number > 56 and chip.player != "pink":
                            chip.cell_number -= 56
                        elif (chip.count > 56 and chip.count < 98) and chip.player == "pink" and not chip.on_finish:
                            chip.cell_number = 99 + (chip.count - 56)
                        if chip.player == "pink" and chip.count > 61:
                            chip.kill()
                            players_chips["pink"][1] -= 1

                        if (chip.count > 56 and chip.count < 98) and chip.player == "green" and not chip.on_finish:
                            chip.cell_number = 199 + (chip.count - 56)
                        if chip.player == "green" and chip.cell_number > 205:
                            chip.kill()
                            players_chips["green"][1] -= 1

                        if (chip.count > 56 and chip.count < 98) and chip.player == "blue" and not chip.on_finish:
                            chip.cell_number = 299 + (chip.count - 56)
                        if chip.player == "blue" and chip.cell_number > 305:
                            chip.kill()
                            players_chips["blue"][1] -= 1

                        if (chip.count > 56 and chip.count < 98) and chip.player == "yellow" and not chip.on_finish:
                            chip.cell_number = 399 + (chip.count - 56)
                        if chip.player == "yellow" and chip.cell_number > 405:
                            chip.kill()
                            players_chips["yellow"][1] -= 1

                if event.button == 3:
                    for cell in cells:
                        if cell.rect.collidepoint(event.pos) and cell.number == 1.1:
                            if current_player == 0 and players_chips["pink"][0] <= players_chips["pink"][1]:
                                if is_free(1.0):
                                    if dice_values[0]:
                                        chip = Chip("pink", 1)
                                        all_sprites.add(chip)
                                        red_chips.append(chip)
                                        chips.append(chip)
                                        dice_values[0] = 0
                                        players_chips["pink"][0] += 1
                                        make_false(cell.number)
                                    elif dice_values[1]:
                                        chip = Chip("pink", 1)
                                        all_sprites.add(chip)
                                        red_chips.append(chip)
                                        chips.append(chip)
                                        dice_values[1] = 0
                                        players_chips["pink"][0] += 1
                                        make_false(cell.number)
                        if cell.rect.collidepoint(event.pos) and cell.number == 43.1:
                            if current_player == 1 and players_chips["green"][0] <= players_chips["green"][1]:
                                if is_free(43.0):
                                    if dice_values[0]:
                                        chip = Chip("green", 43)
                                        all_sprites.add(chip)
                                        green_chips.append(chip)
                                        chips.append(chip)
                                        dice_values[0] = 0
                                        players_chips["green"][0] += 1
                                        make_false(cell.number)
                                    elif dice_values[1]:
                                        chip = Chip("green", 43)
                                        all_sprites.add(chip)
                                        green_chips.append(chip)
                                        chips.append(chip)
                                        dice_values[1] = 0
                                        players_chips["green"][0] += 1
                                        make_false(cell.number)
                        if cell.rect.collidepoint(event.pos) and cell.number == 29.1:
                            if current_player == 2 and players_chips["blue"][0] <= players_chips["blue"][1]:
                                if is_free(29.0):
                                    if dice_values[0]:
                                        chip = Chip("blue", 29)
                                        all_sprites.add(chip)
                                        blue_chips.append(chip)
                                        chips.append(chip)
                                        dice_values[0] = 0
                                        players_chips["blue"][0] += 1
                                        make_false(cell.number)
                                    elif dice_values[1]:
                                        chip = Chip("blue", 29)
                                        all_sprites.add(chip)
                                        blue_chips.append(chip)
                                        chips.append(chip)
                                        dice_values[1] = 0
                                        players_chips["blue"][0] += 1
                                        make_false(cell.number)
                        if cell.rect.collidepoint(event.pos) and cell.number == 15.1:
                            if current_player == 3 and players_chips["yellow"][0] <= players_chips["yellow"][1]:
                                if is_free(15.0):
                                    if dice_values[0]:
                                        chip = Chip("yellow", 15)
                                        all_sprites.add(chip)
                                        yellow_chips.append(chip)
                                        chips.append(chip)
                                        dice_values[0] = 0
                                        players_chips["yellow"][0] += 1
                                        make_false(cell.number)
                                    elif dice_values[1]:
                                        chip = Chip("yellow", 15)
                                        all_sprites.add(chip)
                                        yellow_chips.append(chip)
                                        chips.append(chip)
                                        dice_values[1] = 0
                                        players_chips["yellow"][0] += 1
                                        make_false(cell.number)

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

        if players_chips["pink"][1] == 0:
            final_text[1] = (165, 300, 'Победил игрок PINK', (11, 0, 77), (250, 250, 30), 1)
            final.finscreen()

        if players_chips["green"][1] == 0:
            final_text[1] = (165, 300, 'Победил игрок GREEN', (11, 0, 77), (250, 250, 30), 1)
            final.finscreen()

        if players_chips["blue"][1] == 0:
            final_text[1] = (165, 300, 'Победил игрок BLUE', (11, 0, 77), (250, 250, 30), 1)
            final.finscreen()

        if players_chips["yellow"][1] == 0:
            final_text[1] = (165, 300, 'Победил игрок YELLOW', (11, 0, 77), (250, 250, 30), 1)
            final.finscreen()

        all_sprites.update()
        screen.fill('brown')
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)

    pygame.quit()
