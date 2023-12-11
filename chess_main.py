"""
Main file for work with chess ai
"""

import pygame
import chess_engine as chess

WIDTH = HEIGHT = 512
DIMENSION = 8 # board is 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animations
IMAGES = {}

'''
Initialize a global dictionary of images
'''

def load_images():
    pieces = ['bishop_b', 'bishop_w', 'king_b', 'king_w', 'knight_b', 'knight_w', 'pawn_b', 'pawn_w', 'queen_b', 'queen_w', 'rook_b', 'rook_w']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load('images/' + piece + ".png"), (SQ_SIZE, SQ_SIZE))

'''
The main driver for our code.
'''

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = chess.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    load_images()
    running = True
    sq_selected = () # no square for now selected
    player_clicks = [] # traking of player clicks

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() # x, y pos 
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2:
                    move = chess.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notaion())
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                    gs.make_move(move)
                    sq_selected = ()
                    player_clicks = []
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gs.undo_move()
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        pygame.display.flip()

'''
Responsible for all the graphics within a current game state
'''

def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)

def draw_board(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[(row+column) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "**":
                screen.blit(IMAGES[piece], pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
