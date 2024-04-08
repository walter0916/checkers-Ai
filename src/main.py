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

def get_row_col_from_mouse(pos):
  x, y = pos
  row = y // SQUARE_SIZE
  col = x // SQUARE_SIZE
  return row, col

def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)


def main():
  run = True
  clock = pygame.time.Clock()
  game = Game(WIN)
  ai_gamemode = False


  while run:
    clock.tick(FPS)

    if game.turn == WHITE and ai_gamemode:
      value, new_board = minimax(game.get_board(), 4 , WHITE, game)
      game.ai_move(new_board)

    if game.winner() != None:
      print(game.winner())
      run = False
    
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

def main_menu():
    while True:
        formated_BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

        WIN.blit(formated_BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("CHECKERS", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 4))

        button_width = 30
        button_height = 100
        button_spacing = 10
        button_x = (WIDTH - button_width) // 2
        button_start_y = HEIGHT // 2

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"),
                              pos=(button_x, button_start_y),
                              text_input="PLAY",
                              font=get_font(50),
                              base_color="#d7fcd4",
                              hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"),
                              pos=(button_x, button_start_y + 2 * (button_height + button_spacing)),
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
                    main()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()