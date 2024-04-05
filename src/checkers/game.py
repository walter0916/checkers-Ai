import pygame
from .constants import RED, WHITE
from checkers.board import Board

class Game:
  def __init__(self, win):
    self._init()
    self.win = win

  def update(self):
    self.board.draw(self.win)
    pygame.display.update()
  
  def _init(self):
    self.selected = None
    self.board = Board()
    self.turn = RED
    self.valid_moves = {}

  def reset(self):
    self._init()

