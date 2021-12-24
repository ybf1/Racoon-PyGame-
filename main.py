import pygame


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



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((450, 450))

    all_sprites = pygame.sprite.Group()

    load_field()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()