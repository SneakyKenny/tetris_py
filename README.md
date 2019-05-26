# tetris_py
A random tetris made in command line with python 3.7.1

run by going in src and executing ./main.py

make clean to remove compiled python files

# __Duck optimisation__

modules imported ("requirements"):
- curses (environment to draw the board and just the tetris game overall)
- tkinter (read keyboard input)
- os (call console 'clear' command)
- time
- random

#TODO:
- more scoring methods (modern tetris like)
- lock delay
- das/arr (almost implemented, must make it depend on time and not windows key held thingy)
- gargabe
- game modes (rnjesus: 2nd player controls pieces to come for the tetris player, while he tries to complete missions)
- some sort of IA to battle ?
- bonuses ? (bananatris: spin the board/matrix)

finaly goal:
- jstris/nullpomino like (gameplay wise)
- multiplayer

known issues:
- last line not drawing as intended
- when holding a piece, it might happen that the piece held sticks to the field
