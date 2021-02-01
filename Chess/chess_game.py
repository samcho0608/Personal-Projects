import pygame, os
from pieces import *

pygame.init()

screen_width = 750
screen_height = 780
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Chess Game")

# Game Set Up
game_board = Game(screen)
game_font = pygame.font.Font(None,30)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game_board.option_phase:
                game_board.option_phase = False
                game_board.options.clear()

    if pygame.mouse.get_pressed()[0]:
        m_pos = pygame.mouse.get_pos()
        if not game_board.option_phase:
            side = game_board.black if game_board.black_turn else game_board.white
            for piece in side:
                if piece.clicked(m_pos):
                    piece.show_option()
                    game_board.option_phase = True
        else:
            for o in game_board.options:
                if o.clicked(m_pos):
                    o.piece.move(o.coord)
                    game_board.option_phase = False
                    game_board.options.clear()
                    game_board.black_turn = not game_board.black_turn

    turn_text = game_font.render("Turn: {side} Phase: {phase}".format(\
        side = "Black" if game_board.black_turn else "White", phase = "Option" if game_board.option_phase else "Piece Choice")\
            ,True, (255,255,255))

    # collision
    if not any(isinstance(piece, King) for piece in game_board.white):
        winner = "Black Won!"
        running = False
    if not any(isinstance(piece, King) for piece in game_board.black):
        winner = "White Won!"
        running = False
    
    

    game_board.update()
    screen.blit(turn_text,(0,750)) #((screen_width - turn_text.get_width())/2, 750))

    pygame.display.update()


msg = game_font.render(winner, True, (255,255,0))
msg_rect = msg.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()


pygame.time.delay(2000)

# pygame 종료
pygame.quit()