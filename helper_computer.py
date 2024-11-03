import pygame

window_width = 500
window_height = 500
num_of_columns = 10
num_of_rows = num_of_columns * (window_height / window_width)
block_width = window_width / num_of_columns
block_length = window_height / num_of_rows
block_size = (block_width, block_length)
num_of_bombs = 5
FPS = 120
close_time = 1


class Block():
    def __init__(self, hidden_image, visible_image, flag_image, block_size, x, y, hidden, flagged) -> None:
        self.hidden_sprite = pygame.transform.scale(pygame.image.load(hidden_image), block_size).convert()
        self.visible_sprite = pygame.transform.scale(pygame.image.load(visible_image), block_size).convert()
        self.flag_sprite = pygame.transform.scale(pygame.image.load(flag_image), block_size).convert()
        self.hitbox = self.hidden_sprite.get_rect()
        self.hitbox.center = (x, y)
        self.hidden = hidden
        self.flagged = flagged

    def flag(self):
        if self.flagged:
            self.flagged = False
        else:
            self.flagged = True


class Bomb(Block):
    def __init__(self, hidden_image, visible_image, flag_image, block_size, x, y, hidden, flagged) -> None:
        super().__init__(hidden_image, visible_image, flag_image, block_size, x, y, hidden, flagged)
        self.kind = "bomb"

    def dig(self, block_list):
        self.hidden = False


class Blank(Block):
    def __init__(self, hidden_image, visible_image, flag_image, block_size, x, y, hidden, flagged, neighbours) -> None:
        super().__init__(hidden_image, visible_image, flag_image, block_size, x, y, hidden, flagged)
        self.kind = "blank"
        self.neighbours = neighbours

    def dig(self, block_list):
        self.hidden = False
        for block in block_list:
            if block.hitbox.center in self.neighbours and block.hidden:
                block.dig(block_list)


class Number(Block):
    def __init__(self, hidden_image, visible_image, flag_image, block_size, x, y, hidden, flagged, neighbours, value) -> None:
        super().__init__(hidden_image, visible_image, flag_image, block_size, x, y, hidden, flagged)
        self.kind = "number"
        self.neighbours = neighbours
        self.value = value

    def dig(self, block_list):
        self.hidden = False
