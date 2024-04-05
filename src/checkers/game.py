import pygame
from .constants import RED, WHITE
from board import Board

class Game:
  def __init__(self, win):
    self.selected = None
    self.board = Board()
    self.turn = RED
    self.valid_moves = {}
    self.win = win

  def update(self):
    self.board.draw()
    pygame.display.update()