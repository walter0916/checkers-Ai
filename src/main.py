import pygame
import sys
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE
from checkers.game import Game
from minimax.algorithm import minimax
from button import Button

pygame.init()

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
BG = pygame.image.load("assets/Background.png")

ai_gamemode = False

def get_row_col_from_mouse(pos):
  x, y = pos
  row = y // SQUARE_SIZE
  col = x // SQUARE_SIZE
  return row, col

def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)


def play():
  run = True
  clock = pygame.time.Clock()
  game = Game(WIN)
  global ai_gamemode


  while run:
    clock.tick(FPS)

    if game.turn == WHITE and ai_gamemode:
      alpha = float('-inf')
      beta = float('inf')
      value, new_board = minimax(game.get_board(), 3 ,alpha, beta, WHITE, game)
      game.ai_move(new_board)

    if game.winner() != None:
      run = False
      winner = game.winner()
      game_over_screen(winner)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        main_menu()
      
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        row, col = get_row_col_from_mouse(pos)
        game.select(row, col)
      
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_g:
          ai_gamemode = not ai_gamemode


    game.update()
  
  pygame.quit()

def options():
  global ai_gamemode

  while True:
    formated_BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    WIN.blit(formated_BG, (0, 0))
    OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

    OPTIONS_TEXT = get_font(45).render("SELECT GAME MODE", True, "Black")
    OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    WIN.blit(OPTIONS_TEXT, OPTIONS_RECT)

    button_width = 30
    button_height = 100
    button_spacing = 20
    button_x = (WIDTH - button_width) // 2
    button_start_y = HEIGHT // 2

    OPTIONS_BACK = Button(image=pygame.image.load("assets/Play Rect.png"), 
                              pos=(button_x, button_start_y),
                              text_input="BACK",
                              font=get_font(50),
                              base_color="#d7fcd4",
                              hovering_color="White")
        

    AI_GAMEMODE_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"),
                              pos=(button_x, button_start_y + button_height + button_spacing),
                              text_input="AI",
                              font=get_font(50),
                              base_color="#d7fcd4",
                              hovering_color="White")
        
    PVP_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"),
                              pos=(button_x, button_start_y + 2 * (button_height + button_spacing)),
                              text_input="PVP",
                              font=get_font(50),
                              base_color="#d7fcd4",
                              hovering_color="White")

    for button in [AI_GAMEMODE_BUTTON, PVP_BUTTON, OPTIONS_BACK]:
      button.changeColor(OPTIONS_MOUSE_POS)
      button.update(WIN)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
          main_menu()
        if AI_GAMEMODE_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
          ai_gamemode = True
          play()
        if PVP_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
          ai_gamemode = False
          play()

    pygame.display.update()

def game_over_screen(winner):
  while True:
    formated_BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    WIN.blit(formated_BG, (0, 0))

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    MENU_TEXT = get_font(70).render("Game Over!", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 4))

    winner_text = get_font(30).render(f"{winner} is the winner", True, "#b68f40")
    winner_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    button_width = 30
    button_height = 100
    button_spacing = 20
    button_x = (WIDTH - button_width) // 2
    button_start_y = HEIGHT * 3 // 4

    PLAY_AGAIN_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"),
                                    pos=(button_x, button_start_y),
                                    text_input="Play Again",
                                    font=get_font(30),
                                    base_color="#d7fcd4",
                                    hovering_color="White")
    QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"),
                                pos=(button_x, button_start_y + button_height + button_spacing),
                                text_input="Quit",
                                font=get_font(30),
                                base_color="#d7fcd4",
                                hovering_color="White")

    WIN.blit(MENU_TEXT, (MENU_RECT.centerx - MENU_RECT.width // 2, MENU_RECT.y))
    WIN.blit(winner_text, (winner_rect.centerx - winner_rect.width // 2, winner_rect.y))

    for button in [PLAY_AGAIN_BUTTON, QUIT_BUTTON]:
      button.changeColor(MENU_MOUSE_POS)
      button.update(WIN)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if PLAY_AGAIN_BUTTON.checkForInput(MENU_MOUSE_POS):
          options()
        if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
          pygame.quit()
          sys.exit()

    pygame.display.update()


def main_menu():
  while True:
    formated_BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    WIN.blit(formated_BG, (0, 0))

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    MENU_TEXT = get_font(100).render("CHECKERS", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 4))

    button_width = 30
    button_height = 100
    button_spacing = 20
    button_x = (WIDTH - button_width) // 2
    button_start_y = HEIGHT // 2

    PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"),
                              pos=(button_x, button_start_y),
                              text_input="PLAY",
                              font=get_font(50),
                              base_color="#d7fcd4",
                              hovering_color="White")
    QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"),
                              pos=(button_x, button_start_y + button_height + button_spacing),
                              text_input="QUIT",
                              font=get_font(50),
                              base_color="#d7fcd4",
                              hovering_color="White")

    text_offset_x = MENU_RECT.width // 2
    WIN.blit(MENU_TEXT, (MENU_RECT.centerx - text_offset_x, MENU_RECT.y))

    for button in [PLAY_BUTTON, QUIT_BUTTON]:
      button.changeColor(MENU_MOUSE_POS)
      button.update(WIN)
        
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
          options()
        if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
          pygame.quit()
          sys.exit()

    pygame.display.update()

main_menu()