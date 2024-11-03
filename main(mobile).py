from helper_mobile import *
import random
import pygame
import time
import sys
import os

# Configs

pygame.init()
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()
sys.setrecursionlimit(10000)

# Game Stuff

gamelost = False
gamedone = False
close_timer = 0
close_test = [number * FPS for number in range(1, close_time + 1)]
double_click_time = 0.25
double_click = False
double_click_timer = 0
double_click_timer_started = False
selected_block = None

# Images

image_dict = {"hidden_image": "Assets" + os.sep + "hidden.png",
                              "blank_image": "Assets" + os.sep + "blank.png",
                              "bomb_image": "Assets" + os.sep + "bomb.png",
                              "number_image_list": ["Assets" + os.sep + "1.png", "Assets" + os.sep + "2.png",
                                                                              "Assets" + os.sep + "3.png", "Assets" + os.sep + "4.png",
                                                                              "Assets" + os.sep + "5.png", "Assets" + os.sep + "6.png",
                                                                              "Assets" + os.sep + "7.png", "Assets" + os.sep + "8.png"],
                               "flag_image": "Assets" + os.sep + "flag.png",
                               "cross_image": "Assets" + os.sep + "cross.png",
                               "status_flag_image": "Assets" + os.sep + "status_flag.png",
                               "status_clock_image": "Assets" + os.sep + "status_clock.png"
                               }
cross_sprite = pygame.transform.scale(pygame.image.load(image_dict["cross_image"]), block_size).convert()

# Music

pygame.mixer.set_num_channels(10)
explosion_sfx = pygame.mixer.Sound("Assets" + os.sep + "explosion.mp3")
dig_sfx = pygame.mixer.Sound("Assets" + os.sep + "dig.mp3")
flag_put_sfx = pygame.mixer.Sound("Assets" + os.sep + "flag_put.mp3")
flag_took_sfx = pygame.mixer.Sound("Assets" + os.sep + "flag_took.mp3")
victory_sfx = pygame.mixer.Sound("Assets" + os.sep + "victory.mp3")

# Status Bar

font = "Assets" + os.sep + "freesansbold.ttf"
font_color = (255, 255, 255)
status_color = (89, 89, 89)
status_rect = pygame.Rect(0, 0, window_width, block_length)
status_font = pygame.font.Font(font, int((3 / 4) * block_length))
flag_text = status_font.render(str(num_of_bombs), True, font_color)
flag_text_rect = flag_text.get_rect()
flag_text_rect.center = (window_width / 4, block_length / 2)
status_flag_sprite = pygame.transform.scale(pygame.image.load(image_dict["status_flag_image"]), block_size).convert_alpha()
status_flag_rect = status_flag_sprite.get_rect()
status_flag_rect.center = (flag_text_rect.left - status_flag_rect.width / 2, block_length / 2)

frame_counter = 0
game_timer = 0
clock_text = status_font.render(str(game_timer), True, font_color)
clock_text_rect = clock_text.get_rect()
clock_text_rect.center = (window_width * (3 / 4), block_length / 2)
status_clock_sprite = pygame.transform.scale(pygame.image.load(image_dict["status_clock_image"]), block_size).convert_alpha()
status_clock_rect = status_clock_sprite.get_rect()
status_clock_rect.center = (clock_text_rect.left - status_clock_rect.width / 2, block_length / 2)

# Bomb

bomb_list = []

print("Bomb Generation Started...")
t1 = time.time()
for i in range(num_of_bombs):
    x = random.randrange(int(block_width / 2), window_width, int(block_width))
    y = random.randrange(block_length + int(block_length / 2), window_height, int(block_length))
    while (x, y) in [bomb.hitbox.center for bomb in bomb_list]:
        x = random.randrange(int(block_width / 2), window_width, int(block_width))
        y = random.randrange(block_length + int(block_length / 2), window_height, int(block_length))
    bomb_list.append(Bomb(image_dict["hidden_image"], image_dict["bomb_image"], image_dict["flag_image"], block_size, x, y, True, False))
t2 = time.time()
print(f"Bombs Generated In: {t2 - t1}")

# Number and Blank

number_list = []
blank_list = []

print("Level Genration Started")
t1 = time.time()
for x in range(int(block_width / 2), window_width, int(block_width)):
    for y in range(int(block_length) + int(block_length / 2), window_height, int(block_length)):
        if (x, y) not in [bomb.hitbox.center for bomb in bomb_list]:
            neighbours = [(x - block_width, y - block_length), (x, y - block_length), (x + block_width, y - block_length),
                          (x - block_width, y), (x + block_width, y),
                          (x - block_width, y + block_length), (x, y + block_length), (x + block_width, y + block_length)]
            n_bombs = 0
            for neighbour in neighbours:
                if neighbour in [bomb.hitbox.center for bomb in bomb_list]:
                    n_bombs += 1
            if n_bombs == 0:
                blank_list.append(Blank(image_dict["hidden_image"], image_dict["blank_image"], image_dict["flag_image"], block_size, x, y, True, False, neighbours))
            else:
                number_list.append(Number(image_dict["hidden_image"], image_dict["number_image_list"][n_bombs - 1], image_dict["flag_image"], block_size, x, y, True, False, neighbours, n_bombs))
t2 = time.time()
print(f"Level Generated In: {t2 - t1}")

block_list = bomb_list + blank_list + number_list
num_of_blocks = len(block_list)
print(f"Number Of Blocks: {num_of_blocks}")

while True:
    window.fill((126, 126, 126))
    pygame.draw.rect(window, status_color, status_rect)
    window.blit(flag_text, flag_text_rect)
    window.blit(status_flag_sprite, status_flag_rect)
    window.blit(clock_text, clock_text_rect)
    window.blit(status_clock_sprite, status_clock_rect)

    for block in block_list:
        if not block.hidden:
            window.blit(block.visible_sprite, block.hitbox)
        elif block.flagged:
            window.blit(block.flag_sprite, block.hitbox)
        else:
            window.blit(block.hidden_sprite, block.hitbox)

    for event in pygame.event.get():
        if not gamedone:
            if event.type == pygame.FINGERDOWN and not double_click_timer_started:
                x, y = event.x * window_width, event.y * window_height
                for block in block_list:
                    if block.hitbox.collidepoint(x, y):
                        selected_block = block
                        double_click_timer_started = True
            elif event.type == pygame.FINGERDOWN and double_click_timer_started:
                x, y = event.x * window_width, event.y * window_height
                if selected_block.hitbox.collidepoint(x, y):
                    if not selected_block.flagged:
                        pygame.mixer.Channel(2).play(dig_sfx)
                        selected_block.dig(block_list)
                        if selected_block in bomb_list:
                            pygame.mixer.Channel(1).play(explosion_sfx)
                            gamedone = True
                            gamelost = True
                            print("LOST")
                    if selected_block.kind == "number" and not selected_block.hidden:
                        if len([block for block in block_list if block.hitbox.center in selected_block.neighbours and block.flagged]) == selected_block.value:
                            for block in block_list:
                                if block.hitbox.center in selected_block.neighbours and not block.flagged:
                                    pygame.mixer.Channel(2).play(dig_sfx)
                                    block.dig(block_list)
                                    if block in bomb_list:
                                        pygame.mixer.Channel(1).play(explosion_sfx)
                                        gamedone = True
                                        gamelost = True
                                        print("LOST")
                else:
                    selected_block.flag()
                    if selected_block.flagged:
                        pygame.mixer.Channel(3).play(flag_put_sfx)
                        num_of_bombs -= 1
                        flag_text = status_font.render(str(num_of_bombs), True, font_color)
                        flag_text_rect = flag_text.get_rect()
                        flag_text_rect.center = (window_width / 4, block_length / 2)
                    elif not selected_block.flagged:
                        pygame.mixer.Channel(4).play(flag_took_sfx)
                        num_of_bombs += 1
                        flag_text = status_font.render(str(num_of_bombs), True, font_color)
                        flag_text_rect = flag_text.get_rect()
                        flag_text_rect.center = (window_width / 4, block_length / 2)
                    for block in block_list:
                        if block.hitbox.collidepoint(x, y) and block.hidden:
                            block.flag()
                            if block.flagged:
                                pygame.mixer.Channel(3).play(flag_put_sfx)
                                num_of_bombs -= 1
                                flag_text = status_font.render(str(num_of_bombs), True, font_color)
                                flag_text_rect = flag_text.get_rect()
                                flag_text_rect.center = (window_width / 4, block_length / 2)
                            elif not block.flagged:
                                pygame.mixer.Channel(4).play(flag_took_sfx)
                                num_of_bombs += 1
                                flag_text = status_font.render(str(num_of_bombs), True, font_color)
                                flag_text_rect = flag_text.get_rect()
                                flag_text_rect.center = (window_width / 4, block_length / 2)
                double_click_timer = 0
                double_click_timer_started = False

            if [False] * len(blank_list + number_list) == [block.hidden for block in (blank_list + number_list)]:
                pygame.mixer.Channel(5).play(victory_sfx)
                gamedone = True
                print("WON")

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not gamedone:
        frame_counter += 1
        if frame_counter % FPS == 0:
            game_timer += 1
            clock_text = status_font.render(str(game_timer), True, font_color)
            clock_text_rect = clock_text.get_rect()
            clock_text_rect.center = (window_width * (3 / 4), block_length / 2)
        if double_click_timer_started:
            double_click_timer += 1
        if double_click_timer >= FPS * double_click_time:
            selected_block.flag()
            if selected_block.flagged:
                pygame.mixer.Channel(3).play(flag_put_sfx)
                num_of_bombs -= 1
                flag_text = status_font.render(str(num_of_bombs), True, font_color)
                flag_text_rect = flag_text.get_rect()
                flag_text_rect.center = (window_width / 4, block_length / 2)
            elif not selected_block.flagged:
                pygame.mixer.Channel(4).play(flag_took_sfx)
                num_of_bombs += 1
                flag_text = status_font.render(str(num_of_bombs), True, font_color)
                flag_text_rect = flag_text.get_rect()
                flag_text_rect.center = (window_width / 4, block_length / 2)
            double_click_timer = 0
            double_click_timer_started = False

    if gamedone:
        if gamelost:
            [bomb.dig(block_list) for bomb in bomb_list if not bomb.flagged]
            for block in (blank_list + number_list):
                if block.flagged:
                    block.flag_sprite = cross_sprite
        close_timer += 1
        if close_timer in close_test:
            print(f"Seconds Before Closing: {int(close_test[-(close_test.index(close_timer) + 1)] / FPS)}")
        if close_timer == FPS * (close_time + 1):
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(FPS)
