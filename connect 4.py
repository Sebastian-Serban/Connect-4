import numpy as np
from numpy.lib.index_tricks import _fill_diagonal_dispatcher  
import pygame       
import sys        
import math

from pygame.constants import QUIT         
# GAME INITIALIZATION
pygame.init()
pygame.font.init()

# GLOBALS VARS
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)

# COLORS
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# SCREEN
screen = pygame.display.set_mode(size)

# CAPTION AND ICON
pygame.display.set_caption('Connect Four')


# FONT
myfont = pygame.font.SysFont("monospace", 75)

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def print_board(board):
    print(np.flip(board, 0))

def invalid_board(board):
    status = True
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == 0:
                status = False
    return status

def valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece



def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE +SQUARESIZE/2)), RADIUS )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE  +SQUARESIZE/2)), RADIUS )
            if board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE  +SQUARESIZE/2)), RADIUS )
    pygame.display.update()

def player_wins(board, player):
    # check horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True
    # check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                return True
    # check NE-SW diagonal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True
    # check NE-SW diagonal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(3,ROW_COUNT):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True


board = create_board()
print_board(board)
game_on = True
turn = 0

draw_board(board)
pygame.display.update()

while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)

        if invalid_board(board):
            label = myfont.render("Draw game", 1, BLUE)
            screen.blit(label, (50,10))
            game_on = False


        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            if turn == 0:
                posx =  event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if player_wins(board, 1):
                        label = myfont.render("Player 1 wins!", 1, RED)
                        screen.blit(label, (50,10))
                        game_on = False

            else:
                posx =  event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if player_wins(board, 2):
                        label = myfont.render("Player 2 wins!", 1, RED)
                        screen.blit(label, (50,10))
                        game_on = False
            

            draw_board(board)
            print_board(board)
            turn += 1
            turn = turn % 2

            if game_on:
                pygame.time.wait(1000)
