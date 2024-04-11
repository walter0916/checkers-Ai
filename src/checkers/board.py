import pygame
from .constants import BLACK, ROWS,COLS, RED, SQUARE_SIZE, WHITE
from .piece import Piece
from minimax.algorithm import get_all_moves

class Board:
  def __init__(self):
    self.board = []
    self.selected_pieces = None
    self.red_left = self.white_left = 12
    self.red_kings = self.white_kings = 0
    self.create_board()

  def draw_squares(self, win):
    win.fill(BLACK)
    for row in range(ROWS):
      for col in range(row % 2, COLS, 2):
        pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
  
  def evaluate(self, board, game):
    white_mobility = len(get_all_moves(board, WHITE, game))
    red_mobility = len(get_all_moves(board, RED, game))
    mobility_score = white_mobility - red_mobility

    white_pieces = len(board.get_all_pieces(WHITE))
    red_pieces = len(board.get_all_pieces(RED))
    piece_count_score = white_pieces - red_pieces

    white_kings = sum(piece.king for piece in board.get_all_pieces(WHITE))
    red_kings = sum(piece.king for piece in board.get_all_pieces(RED))
    king_count_score = (white_kings * 0.5) - (red_kings * 0.5)

    white_advancement = sum(piece.row / 7 for piece in board.get_all_pieces(WHITE))
    red_advancement = sum((7 - piece.row) / 7 for piece in board.get_all_pieces(RED))
    king_advancement_score = white_advancement - red_advancement

    white_center_control = sum(1 for piece in board.get_all_pieces(WHITE) if 2 <= piece.col <= 5)
    red_center_control = sum(1 for piece in board.get_all_pieces(RED) if 2 <= piece.col <= 5)
    center_control_score = white_center_control - red_center_control

    score = (
        mobility_score * 1 +
        piece_count_score * 2 +
        king_count_score * 3 +
        king_advancement_score * 1 +
        center_control_score * 2
    )

    return score

  def get_all_pieces(self, color):
    pieces = []
    for row in self.board:
      for piece in row:
        if piece != 0 and piece.color == color:
          pieces.append(piece)
    return pieces

  def move(self, piece, row, col):
    self.board[piece.row][piece.col], self.board[row][col]= self.board[row][col], self.board[piece.row][piece.col]
    piece.move(row, col)

    if row == ROWS - 1 or row == 0:
      if not piece.king:
        piece.make_king()
        if piece.color == WHITE:
          self.white_kings += 1
        else:
          self.red_kings += 1

  def get_piece(self, row, col):
    return self.board[row][col]

  def create_board(self):
    for row in range(ROWS):
      self.board.append([])
      for col in range(COLS):
        if col % 2 == ((row + 1) % 2):
          if row < 3: 
            self.board[row].append(Piece(row, col, WHITE))
          elif row > 4: 
            self.board[row].append(Piece(row, col, RED))
          else: 
            self.board[row].append(0)
        else:
          self.board[row].append(0)
  
  def draw(self, win):
    self.draw_squares(win)
    for row in range(ROWS):
      for col in range(COLS):
        piece = self.board[row][col]
        if piece != 0:
          piece.draw(win)

  def remove(self, pieces):
    for piece in pieces:
      self.board[piece.row][piece.col] = 0
      if piece != 0:
        if piece.color == RED:
          self.red_left -= 1
        else:
          self.white_left -= 1

  def winner(self):
    if self.red_left <= 0:
      return WHITE
    elif self.white_left <= 0:
      return RED
    
    return None

  def get_valid_moves(self, piece):
    moves = {}
    left = piece.col - 1
    right = piece.col + 1
    row = piece.row

    if piece.color == RED or piece.king:
      moves.update(self._transverse_left(row - 1, max(row-3, -1), -1, piece.color, left))
      moves.update(self._transverse_right(row - 1, max(row-3, -1), -1, piece.color, right))

    if piece.color == WHITE or piece.king:
      moves.update(self._transverse_left(row + 1, min(row+3, ROWS), 1, piece.color, left))
      moves.update(self._transverse_right(row + 1, min(row+3, ROWS), 1, piece.color, right))
    
    return moves

  def _transverse_left(self, start, stop, step, color, left, skipped=[]):
    moves = {}
    last = []
    for r in range(start, stop ,step):
      if left < 0:
        break

      current = self.board[r][left]
      if current == 0:
        if skipped and not last:
          break
        elif skipped:
          moves[(r, left)] = last + skipped
        else:
          moves[(r, left)] = last
        
        if last:
          if step == -1:
            row = max(r-3, -1)
          else:
            row = min(r+3, ROWS)

          if skipped: 
            moves.update(self._transverse_left(r+step, row, step, color, left-1, skipped=last+skipped))
            moves.update(self._transverse_right(r+step, row, step, color, left+1, skipped=last+skipped))
          else:
            moves.update(self._transverse_left(r+step, row, step, color, left-1, skipped=last))
            moves.update(self._transverse_right(r+step, row, step, color, left+1, skipped=last))

        break

      elif current.color == color:
        break
      else:
        last = [current]
      
      left -= 1

    return moves

  def _transverse_right(self, start, stop, step, color, right, skipped=[]):
    moves = {}
    last = []
    for r in range(start, stop ,step):
      if right >= COLS:
        break

      current = self.board[r][right]
      if current == 0:
        if skipped and not last:
          break
        elif skipped:
          moves[(r, right)] = last + skipped
        else:
          moves[(r, right)] = last
        
        if last:
          if step == -1:
            row = max(r-3, -1)
          else:
            row = min(r+3, ROWS)
          
          if skipped:
            moves.update(self._transverse_left(r+step, row, step, color, right-1, skipped=last+skipped))
            moves.update(self._transverse_right(r+step, row, step, color, right+1, skipped=last+skipped))
          else:
            moves.update(self._transverse_left(r+step, row, step, color, right-1, skipped=last))
            moves.update(self._transverse_right(r+step, row, step, color, right+1, skipped=last))
        break

      elif current.color == color:
        break
      else:
        last = [current]
      
      right += 1
    
    return moves