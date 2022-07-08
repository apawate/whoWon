import pygame
from PIL import Image


class Key(pygame.sprite.Sprite):
    def __init__(self, x_pos):
        super(Key, self).__init__()
        self.clicked = False
        self.xpos = x_pos
        self.rect = pygame.Rect((self.xpos, 0), (2, 1000))


RED = (255, 0, 0)
BLACK = (0, 0, 0)
pygame.init()
FILE_PATH = input("Enter the file path to the image: ")
original_image = Image.open(FILE_PATH)

X = original_image.width
Y = original_image.height

display_window = pygame.display.set_mode((1900, Y))
pygame.display.set_caption("Finish_Image")
img = pygame.image.load(FILE_PATH)

init_x_position = X * (-1) + 1900
x_position = init_x_position

key_list = pygame.sprite.Group()

display_window.fill(BLACK)

display_window.blit(img, (x_position, 0))

while True:

    display_window.fill(BLACK)

    display_window.blit(img, (x_position, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
            quit()

        # Line Dragging
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            if event.button == 3:
                key_list.add(Key(x))
            elif event.button == 1:
                for key in key_list:
                    if key.rect.collidepoint(x, y):
                        key.clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            for key in key_list:
                key.clicked = False

            # Left and right scrolling
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if x_position > init_x_position:
                    x_position -= 100
                    for key in key_list:
                        left_edge = key.rect.left
                        key.rect = pygame.Rect((left_edge - 100, 0), (2, 1000))
                else:
                    delta = x_position - init_x_position
                    x_position = init_x_position
                    for key in key_list:
                        left_edge = key.rect.left
                        key.rect = pygame.Rect((left_edge - delta, 0), (2, 1000))

            if event.key == pygame.K_LEFT:
                if x_position < -100:
                    x_position += 100
                    for key in key_list:
                        left_edge = key.rect.left
                        key.rect = pygame.Rect((left_edge + 100, 0), (2, 1000))
                else:
                    for key in key_list:
                        left_edge = key.rect.left
                        key.rect = pygame.Rect((left_edge - x_position, 0), (2, 1000))
                    x_position = 0

    for key in key_list:
        if key.clicked:
            pos = pygame.mouse.get_pos()
            key.rect = pygame.Rect((pos[0], 0), (2, 1000))
        pygame.draw.rect(display_window, RED, key.rect)

    pygame.display.update()
