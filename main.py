import pygame


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 600))

    cell1 = Cell(10, 10)
    cell2 = Cell(40, 10)
    cell3 = Cell(70, 10)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(cell1)
    all_sprites.add(cell2)
    all_sprites.add(cell3)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()