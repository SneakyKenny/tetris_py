CC = g++
CFLAGS = -Wall -Wextra -std=c++2a -pedantic -Werror -g3
CPPFLAGS = -lncurses

SRC = \
	  src/tetris/board.cc	\

OBJ = $(SRC:.cc=.o)

INCLUDE = \
		  src/include	\

INCLUDE_FLAGS = $(INCLUDE:%=-I%)

TARGET = cpptris

.PHONY: all clean

all:
	$(CC) src/main.cc $(SRC) $(CFLAGS) $(CPPFLAGS) $(INCLUDE_FLAGS) -o $(TARGET)

clean:
	@$(RM) $(shell find -name '*.o') $(TARGET)
