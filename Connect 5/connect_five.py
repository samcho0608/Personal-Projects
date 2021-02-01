import pygame, os
from board import *
from stone import *

# 화면 크기 설정
screen_width = 800
screen_height = 800

def main():
    pygame.init() # 반드시 필요

    screen = pygame.display.set_mode((screen_width, screen_height))

    #FPS
    clock = pygame.time.Clock()
    
    # Game title
    pygame.display.set_caption("오목")

    # Game Board
    board = Board()

    stone = None
    running = True
    while running and not board.won:
        dt = clock.tick(60) # 게임 화면의 초당 프레임 수 설정

        # Event control
        for event in pygame.event.get():
            # Terminate game once window closes
            if event.type == pygame.QUIT:
                running = False

            # When mouse clicked or there is a stone on the mouse
            if event.type == pygame.MOUSEBUTTONDOWN or stone:
                coord = pygame.mouse.get_pos()
                stone = Stone(board.turn, coord[0], coord[1])

            # When mouse click released
            if event.type == pygame.MOUSEBUTTONUP:
                coord = pygame.mouse.get_pos()
                coord = [ int((i - 3) // 42) for i in coord ]
                board.place_stone(coord[0], coord[1])
                stone = None

        # blit all images
        board.blit(screen)
        if stone:
            screen.blit(stone.image, (stone.x - 21, stone.y - 21))

        pygame.display.update() # 게임 화면을 다시 그리기!
                                # must be called every loop


if __name__ == "__main__":
    main()