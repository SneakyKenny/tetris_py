#!/usr/bin/env python3.7

#http://harddrop.com/wiki/Category:Game_Mechanics

#from __future__ import print_function
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

import tetris
import custom_tools

import time
import random

from pieces import *
from board import *

from read_config import *
import my_networking
#from threading import Thread
import menu_creator
import game_manager
import read_config
#TODO/FIXME: 180 spins check tspins
#DAS toolkit: 50 = 1 second
#so 10 is 1/5 second = .2s = 200 nullpomino das
#therefore actual das = 1000/nullpomino_das
nullpomino_das = 150
nullpomino_arr = 0
DAS_value = 25 / nullpomino_das
ARR_value = nullpomino_arr / 25

(width, height) = (460, 500)

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
    global start_time
    start_time = time.time()
    global t
    t = tetris.Tetris()
    t.spawn_next_piece(isFirstPiece = True)
    return t

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

def quit_program():
    pygame.quit()
    quit()

def main():

    username_list = ['Bob', 'John', 'Noob', 'Master', '6969','Gamer','Mr. Pajitnov','Alexey','sal-T']
    username = None#username_list[random.randint(0, len(username_list))]

    try:
        username = read_config.read_config('settings.ini', 'SectionUserInfos')['username']
    except:
        username = input('Username:')
        if not (username and len(username) > 0 and len(username) < 32):
            username = username_list[random.randint(0, len(username_list))]
            print('No username given, setting it to', username)

        has_wrote = read_config.write_config(file_path = 'settings.ini', section = 'SectionUserInfos', option = 'username', value = username)
        if has_wrote:
            print('Username saved!')
        else:
            print('Failed to save your username, you\'ll have to input it again.')

    global screen
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Pytris')
    screen.fill(background_colour_around)
    pygame.display.flip()
    pygame.key.set_repeat()

    global t, start_time

    t = init_tetris()

    config = read_config.read_config(file_path = 'settings.ini', section = 'SectionKeyBinds')
    for k, b in config.items():
        config[k] = int(b)

    elapsed = 0

    left_held = False
    right_held = False
    left_held_timer = 0
    right_held_timer = 0

    total_time = 0

    server_thread = None
    client = None

    menu_ret = menu_creator.create_menu(screen)
    screen.fill(background_colour_around) # reset screen after the menu is gone

    username = read_config.read_config('settings.ini', 'SectionUserInfos')['username']

    if menu_ret == menu_creator.MenuOptions.IS_JOINING_TEXT:
        client = my_networking.GameClient(username = username, tetris = t)
    elif menu_ret == menu_creator.MenuOptions.IS_PLAYING_SOLO:
        pass
    else:
        server_thread = menu_ret
        client = my_networking.GameClient(username = username, tetris = t)

    running = True
    while running:
        if client and client.is_connected and not client.game_client_loop_check():
            quit_program()

        pygame.draw.rect(screen, background_colour_around, pygame.Rect(score_pos, (score_scale, score_scale)))
        p = t.points
        font_size = 32 - 3 * len(str(p))
        font = pygame.font.SysFont('verdana', font_size)
        ptext = font.render(str(int(p)), True, (255, 255, 255), background_colour_around)
        prect = ptext.get_rect()
        prect.center = (score_pos[0] + score_scale / 2, score_pos[1] + score_scale / 2)
        screen.blit(ptext, prect)

        cur_time = time.time()
        delta = cur_time - start_time
        elapsed += delta

        total_time += elapsed


        t.time_to_check_drop += delta
        if t.has_moved == False:
            t.locktimer += delta

        if t.time_to_check_drop > tetris.time_to_drop_per_level[t.level]:
            t.time_to_check_drop = 0
            if t.times_lock_reset >= 15:
                t.lock_delay(True)
                t.hard_drop_piece()
                t.spawn_next_piece()
            elif not t.move_active_piece():
                if t.locktimer >= t.lockcheck:
                    t.lock_delay(True)
                    t.spawn_next_piece()
                elif t.has_moved == True:
                    t.has_moved = False
                #if (not t.spawn_next_piece()):
                    #quit_program()

            t.cur_rot_is_tspin = False

        start_time = cur_time

        pre_x, pre_y, pre_r = t.active_piece.x,t.active_piece.y, t.active_piece.rot_index


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_program()

            elif event.type == pygame.KEYDOWN:
                if event.key == ord('q') or event.key == pygame.K_ESCAPE:
                    quit_program()

                if not client or (client and not client.is_connected):
                    if event.key == pygame.K_F4:
                        init_tetris()
                if event.key == config['move_left']:#pygame.K_LEFT:
                    left_held = True
                    right_held = False
                    right_held_timer = 0
                    t.move_piece('L')
                if event.key == config['move_right']:#pygame.K_RIGHT:
                    right_held = True
                    left_held = False
                    left_held_timer = 0
                    t.move_piece('R')
                if event.key == config['rotate_left']:#pygame.K_z:
                    t.rotate_piece('L')
                if event.key == config['rotate_right']:#pygame.K_UP:
                    t.rotate_piece('R')
                if event.key == config['rotate_180']:#pygame.K_x:
                    t.rotate_piece('180')
                if event.key == config['hold_piece']:#pygame.K_c:
                    t.hold_piece()
                if event.key == config['hard_drop']:#pygame.K_SPACE:
                    t.hard_drop_piece()
                #TODO: soft_drop + sonic_drop
                if event.key == config['soft_drop']:#pygame.K_DOWN:
                    t.soft_drop_piece()
                if event.key == config['sonic_drop']:#pygame.K_DOWN:
                    t.sonic_drop_piece()
                if event.key == ord('1'):
                    #t.set_active_visibility(None)
                    #t.active_piece = I()
                    t.has_moved = True
                    t.locktimer = 0
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
        if (pre_x != t.active_piece.x or pre_y != t.active_piece.y or pre_r != t.active_piece.rot_index) and not t.has_moved:
            t.lock_delay(False)
        render()

if __name__ == '__main__':
    main()
