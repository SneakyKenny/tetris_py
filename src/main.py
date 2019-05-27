#!/usr/bin/env python3.7

#http://harddrop.com/wiki/Category:Game_Mechanics

#from __future__ import print_function

import pygame

import tetris
import custom_tools

import time

from pieces import *
from board import *

from read_config import *

#DAS toolkit: 50 = 1 second
#so 10 is 1/5 second = .2s = 200 nullpomino das
#therefore actual das = 1000/nullpomino_das
nullpomino_das = 150
nullpomino_arr = 0
DAS_value = 25 / nullpomino_das
ARR_value = nullpomino_arr / 25

(width, height) = (460, 480)

hold_pos = (10, 10)
hold_size = (80, 80)
hold_scale = 20

preview_pos = (350, 10)
preview_size = (100, 100)
preview_scale = 20
num_in_preview = 5

score_pos = (10, 250)
score_scale = 100

scale = 20
border_scale_x = 100
border_scale_y = 10

background_colour_board = (200, 200, 200)
background_colour_around = (150, 150, 150)

def init_tetris():
    global t, start_time
    t = tetris.Tetris()
    t.spawn_next_piece(isFirstPiece = True)
    start_time = time.time()

def draw_rect(i, j, color = (0, 0, 0)):
    global t, screen
    start = (i * scale + border_scale_x + 1, j * scale + border_scale_y + 1)
    size = (scale - 1, scale - 1)
    pygame.draw.rect(screen, color, pygame.Rect(start, size))

def get_piece_color_from_name(name):
    return color_from_board_val[tetris.piece_to_int[name]]

def get_piece_matrix_from_name(name):
    return piece_matrix_list[tetris.piece_to_int[name]]

def draw_piece(pos, scale, p):
    global screen
    col = get_piece_color_from_name(p)
    mat = get_piece_matrix_from_name(p)

    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j]:
                pygame.draw.rect(screen, col, pygame.Rect((j * scale + pos[0], i * scale + pos[1]), (scale - 1, scale - 1)))

def display_hold():
    global t
    p = t.held_piece

    if p:
        draw_piece(hold_pos, hold_scale, p)

def clear_hold_spot():
    global screen

    pygame.draw.rect(screen, background_colour_around, pygame.Rect(hold_pos, (hold_size)))

def display_preview():
    global t
    l = t.get_preview_list(num_in_preview)
    for i in range(num_in_preview):
        draw_piece((preview_pos[0], preview_pos[1] + i * preview_size[1]), preview_scale, l[i])

def clear_preview_spot():
    global screen

    pygame.draw.rect(screen, background_colour_around, pygame.Rect(preview_pos, (350, 470)))

def display_next_pieces_and_hold():
    global t, screen

    clear_hold_spot()

    display_hold()

    clear_preview_spot()

    display_preview()

def render():
    global t, screen
    for i in range(t.board.width + 2):
        draw_rect(i, 0)

    g = t.draw_ghost()

    t.draw_active_piece()

    for i in range(t.board.height):
        draw_rect(0, i + 1)
        draw_rect(t.board.width + 1, i + 1)
        for j in range(t.board.width):
            if t.board.board[i + t.board.hmargin][j] is not None:
                draw_rect(j + 1, i + 1,  color_from_board_val[t.board.board[i + t.board.hmargin][j]])
            else:
                draw_rect(j + 1, i + 1, background_colour_board)

    t.remove_ghost()

    for i in range(t.board.width + 2):
        draw_rect(i, t.board.height + 1)

    display_next_pieces_and_hold()

    pygame.display.flip()

def main():
    global t, start_time

    init_tetris()

    elapsed = 0
    global screen
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Pytris')
    screen.fill(background_colour_around)
    pygame.display.flip()
    pygame.key.set_repeat()

    left_held = False
    right_held = False
    left_held_timer = 0
    right_held_timer = 0

    total_time = 0

    running = True
    while running:
        pygame.draw.rect(screen, background_colour_around, pygame.Rect(score_pos, (score_scale, score_scale)))
        p = t.points
        font_size = 32 - 3 * len(str(p))
        font = pygame.font.SysFont('verdana', font_size)
        ptext = font.render(str(p), True, (255, 255, 255), background_colour_around)
        prect = ptext.get_rect()
        prect.center = (score_pos[0] + score_scale / 2, score_pos[1] + score_scale / 2)
        screen.blit(ptext, prect)

        cur_time = time.time()
        delta = cur_time - start_time

        elapsed += delta

        total_time += elapsed

        if elapsed > tetris.time_to_drop_per_level[t.level]:
            elapsed = 0
            if not t.move_active_piece():
                if not t.spawn_next_piece():
                    running = False
                    pygame.quit()
                    break

            t.cur_rot_is_tspin = False

        start_time = cur_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == ord('q') or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_F4:
                    init_tetris()
                if event.key == pygame.K_LEFT:
                    left_held = True
                    right_held = False
                    right_held_timer = 0
                    t.move_piece('L')
                if event.key == pygame.K_RIGHT:
                    right_held = True
                    left_held = False
                    left_held_timer = 0
                    t.move_piece('R')
                if event.key == pygame.K_z:
                    t.rotate_piece('L')
                if event.key == pygame.K_UP:
                    t.rotate_piece('R')
                if event.key == pygame.K_x:
                    t.rotate_piece('180')
                if event.key == pygame.K_c:
                    t.hold_piece()
                if event.key == pygame.K_SPACE:
                    t.hard_drop_piece()
                if event.key == pygame.K_DOWN:
                    t.soft_drop_piece()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_held = False
                    left_held_timer = 0
                if event.key == pygame.K_RIGHT:
                    right_held = False
                    right_held_timer = 0

        if left_held:
            left_held_timer += delta
        if right_held:
            right_held_timer += delta

        if left_held_timer >= DAS_value:
            t.move_piece('L')
            left_held_timer -= ARR_value
        if right_held_timer >= DAS_value:
            t.move_piece('R')
            right_held_timer -= ARR_value

        render()

if __name__ == '__main__':
    main()
