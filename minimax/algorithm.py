from copy import deepcopy
import pygame
from checkers.board import Board

RED = (255, 0, 0)
WHITE = (255, 255, 255)

def minimax(position, depth, max_player, game):
  if depth == 0 or position.winner() != None:
    return position.evaluate(), position
  
  if max_player:
    maxEval = float('-inf')
    best_move = None
    for move in get_all_moves(position, WHITE):
      pass

  else: 
    return

def get_all_moves(position, color, game):
  moves = []
  board = Board()

  for piece in board.get_all_pieces(position):
    valid_moves = board.get_all_moves(piece)
    for move, skip in valid_moves.items():
      temp_board = deepcopy(board)
      new_board = simulate_move(piece, move, temp_board, game, skip)
      moves.append([new_board, piece])

  return moves