#!/usr/bin/env python3.7

#http://harddrop.com/wiki/Category:Game_Mechanics

#import pygame
#from __future__ import print_function

import curses
from curses import wrapper

import tetris
import custom_tools

import time

from pieces import *

def display_tetris(t, win):
    lines = t.tetris_as_str().split('\n')
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            win.addch(i, j, lines[i][j])

    win.refresh()

def main():
    t = tetris.Tetris()

    t.spawn_next_piece(isFirstPiece = True)

    win = curses.initscr()
    win.clear()
    curses.noecho()
    curses.cbreak()
    win.keypad(True)
    win.nodelay(True)

    display_tetris(t, win)

    start_time = time.time()
    elapsed = 0
    try:
        while True:
            c = win.getch()

            cur_time = time.time()
            delta = cur_time - start_time

            elapsed += delta

            if elapsed > tetris.time_to_drop_per_level[t.level]:
                elapsed = 0
                if not t.move_active_piece():
                    if not t.spawn_next_piece():
                        break

                t.cur_rot_is_tspin = False
                display_tetris(t, win)

            start_time = cur_time

            if c == -1: #with nodelay(True): skips if user hasn't input anything
                continue

            if c == ord('q'):
                break
            t.remove_ghost()

            old_y = t.active_piece.y

            if c == curses.KEY_LEFT:
                t.move_piece('L')
            elif c == curses.KEY_RIGHT:
                t.move_piece('R')
            elif c == curses.KEY_DOWN:
                if t.move_piece('D'):
                    t.cur_rot_is_tspin = False
            elif c == curses.KEY_UP:
                t.rotate_piece('R')
            elif c == ord('z'):
                t.rotate_piece('L')
            elif c == ord('x'):
                t.rotate_piece('180')
            elif c == ord(' '):
                has_moved = False
                while t.move_active_piece():
                    has_moved = True
                if has_moved:
                    t.cur_rot_is_tspin = False
                t.spawn_next_piece()
            elif c == ord('c'):
                t.hold_piece()
            elif c == curses.KEY_F4:
                t = tetris.Tetris()
                t.spawn_next_piece(isFirstPiece = True)

            if t.active_piece.y != old_y:
                elapsed = 0

            display_tetris(t, win)




            if c == ord('1'):
                t.set_invisible()
                t.active_piece = I()
                t.set_visible()
            elif c == ord('2'):
                t.set_invisible()
                t.active_piece = O()
                t.set_visible()
            elif c == ord('3'):
                t.set_invisible()
                t.active_piece = J()
                t.set_visible()
            elif c == ord('4'):
                t.set_invisible()
                t.active_piece = L()
                t.set_visible()
            elif c == ord('5'):
                t.set_invisible()
                t.active_piece = S()
                t.set_visible()
            elif c == ord('6'):
                t.set_invisible()
                t.active_piece = Z()
                t.set_visible()
            elif c == ord('7'):
                t.set_invisible()
                t.active_piece = T()
                t.set_visible()




    finally:
        curses.nocbreak()
        win.keypad(False)
        curses.echo()
        curses.endwin()

if __name__ == '__main__':
    main()
