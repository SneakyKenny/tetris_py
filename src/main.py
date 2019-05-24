#!/usr/bin/env python

#http://harddrop.com/wiki/Category:Game_Mechanics

#import pygame
#from __future__ import print_function

import curses
from curses import wrapper

import tetris
import custom_tools

import time

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
                display_tetris(t, win)

            start_time = cur_time

            if c == -1: #with nodelay(True): skips if user hasn't input anything
                continue

            if c == ord('q'):
                break
            t.remove_ghost()
            if c == curses.KEY_LEFT:
                t.move_piece('L')
            elif c == curses.KEY_RIGHT:
                t.move_piece('R')
            elif c == curses.KEY_DOWN:
                t.move_piece('D')
                elapsed = 0
            elif c == curses.KEY_UP:
                t.rotate_piece('R')
            elif c == ord('z'):
                t.rotate_piece('L')
            elif c == ord('x'):
                t.rotate_piece('180')
            elif c == ord(' '):
                while t.move_active_piece():
                    pass
                t.spawn_next_piece()
            elif c == ord('c'):
                t.hold_piece()

            display_tetris(t, win)

    finally:
        curses.nocbreak()
        win.keypad(False)
        curses.echo()
        curses.endwin()
        print('game over')

if __name__ == '__main__':
    main()
