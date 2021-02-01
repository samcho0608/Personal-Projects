from stone import *
import os, pygame

# BLACK = True
# WHITE = False

class Board:

    def __init__(self):
        self.board = [[None for i in range(19)] for j in range(19)]
        self.screen_coord = [[(i,j) for i in range(5,42*19,42)] for j in range(5,42*19,42)]
        self.won = False
        self.turn = True
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "background.png")),(800,800))


    def place_stone(self, x, y):
        try:
            # if there is a stone at the parameter coordinate, cannot place a stone
            if isinstance(self.board[y][x], Stone):
                return False
            # create a new stone at the parameter coordinate
            self.board[y][x] = Stone(self.turn, x, y)

            # check if the player won
            if self.win(x,y):
                self.won = True
            
            # change the turn once placement complete
            self.turn = not self.turn
            return True
        except Exception:
            return False

    # True if end hit,
    # False if continuable
    def check_end(self, x,y):
        try:
            if any(c < 0 or c >= len(self.board) for c in [x,y]):
                return True
            stone = self.board[y][x]
            return stone.side != self.turn if stone else True
        except Exception as err:
            print(err)
            return True

    # dir
    # 0 1 2
    # 3 5 3
    # 2 1 0

    # check if there was any winning result based on the direction description above
    def win(self, x, y):
        delta = [(-1, -1), (0, -1), (1, -1), (-1, 0)]

        # for every direction
        for i in range(4):
            px = mx = x
            py = my = y
            plus_end = minus_end = False
            dx, dy = delta[i]

            in_a_row = 1    # the original stone itself

            # check each of plus and minus direction
            while not all([plus_end, minus_end]):
                if not plus_end:
                    px += dx
                    py += dy
                    if self.check_end(px, py):
                        plus_end = True
                    else:
                        in_a_row += 1
                
                if not minus_end:
                    mx -= dx
                    my -= dy
                    if self.check_end(mx, my):
                        minus_end = True
                    else:
                        in_a_row += 1

            if in_a_row >= 5:
                return True

        return False


    def __str__(self):
        string = ""
        for i in self.board:
            for j in i:
                if isinstance(j, Stone):
                    string += "B " if j.side else "W "
                else:
                    string += '+ '

            string += "\n"

        return string

    # blit all the images on the screen
    def blit(self, screen):
        screen.blit(self.image, (0,0))
        for row in self.board:
            for stone in row:
                if isinstance(stone, Stone):
                    screen.blit(stone.image, self.screen_coord[stone.y][stone.x])

if __name__ == '__main__':
    b = Board()

    while not b.won:
        print(b)

        print('{} Turn'.format('Black' if b.turn else 'White'))


        while True:
            try:
                coord = input('Input Coordinate: ')
                x,y = tuple(int(i) for i in coord.split(','))

                if b.place_stone(x,y):
                    break
            except:
                print('Invalid Input!')

        b.turn = not b.turn
                    

    # previous turn's side won
    print('{} Won'.format('Black' if not b.turn else 'White'))