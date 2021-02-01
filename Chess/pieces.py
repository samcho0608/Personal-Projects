import os, pygame

# image sprites
dir_path = os.path.dirname(__file__)
images_path = os.path.join(dir_path, "images")
pawn_sprite = pygame.image.load(os.path.join(images_path, "pawn.png"))
white_pawn_sprite = pygame.image.load(os.path.join(images_path, "pawn_white.png"))
knight_sprite = pygame.image.load(os.path.join(images_path, "knight.png"))
white_knight_sprite = pygame.image.load(os.path.join(images_path, "knight_white.png"))
queen_sprite = pygame.image.load(os.path.join(images_path, "queen.png"))
white_queen_sprite = pygame.image.load(os.path.join(images_path, "queen_white.png"))
king_sprite = pygame.image.load(os.path.join(images_path, "king.png"))
white_king_sprite = pygame.image.load(os.path.join(images_path, "king_white.png"))
bishop_sprite = pygame.image.load(os.path.join(images_path, "bishop.png"))
white_bishop_sprite = pygame.image.load(os.path.join(images_path, "bishop_white.png"))
rook_sprite = pygame.image.load(os.path.join(images_path, "rook.png"))
white_rook_sprite = pygame.image.load(os.path.join(images_path, "rook_white.png"))
base = pygame.image.load(os.path.join(images_path, "background_base.png"))
board = pygame.image.load(os.path.join(images_path, "background_board.png"))
background = pygame.image.load(os.path.join(images_path, "background.png"))
square = pygame.image.load(os.path.join(images_path, "board_black_square.png"))
option_sprite = pygame.image.load(os.path.join(images_path, "Picture1.png"))

base_size = base.get_size()
board_size = board.get_size()
square_coord = []
for i in range(0,8):
    for j in range(0,8):
        if i % 2 == 0 and j % 2 != 0:
            square_coord.append((i * 90, j * 90))
        elif i % 2 != 0 and j % 2 == 0:
            square_coord.append((i * 90, j * 90))
board_coord = ((base_size[0] - board_size[0])/2,\
        (base_size[1] - board_size[1])/2)

# Game class contains the board and 2D List of all the pieces
class Game():    
    def __init__(self, screen):
        self.black = []
        self.white = []

        b_side = [
            [Rook("B", self),
            Knight("B", self),
            Bishop("B", self),
            King("B",self),
            Queen("B", self),
            Bishop("B", self),
            Knight("B", self),
            Rook("B", self)],
            [Pawn("B", self) for i in range(8)]
            ]

        w_side = [[piece.copy() for piece in row] for row in b_side]
        w_side.reverse()
        w_side[1].reverse()
        for row in w_side:
            for piece in row:
                piece.changeSide("W")
        self.board = b_side + [[0]* 8 for i in range(4)] + w_side
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if isinstance(piece, Piece):
                    piece.set_coord((i,j))
                    self.black.append(piece) if piece.side == "B" else self.white.append(piece)
        self.screen = screen
        self.option_phase = False
        self.black_turn = True
        self.options = []

    def swap(self, coord1, coord2):
        temp = self.board[coord1[0]][coord1[1]]
        self.board[coord1[0]][coord1[1]] = self.board[coord2[0]][coord2[1]]
        self.board[coord2[0]][coord2[1]] = temp

    def promotion(self):
        promo = False
        for i, j in board[0], board[7]:
            pass

    def update(self):
        # update the screen
        self.screen.blit(background, (0,0))
        self.screen.blit(base, (0,0))
        self.screen.blit(board, board_coord)
        for coord in square_coord:
            self.screen.blit(square, (board_coord[0] + coord[0],\
                board_coord[1] + coord[1]))
        # update all the pieces on the board
        for row in self.board:
            for piece in row:
                if piece != 0:
                    self.screen.blit(piece.sprite, piece.screen_coord)
        
        if self.options is not None:
            for o in self.options:
                self.screen.blit(o.sprite, o.screen_coord)

# class for all objects in the game
class Content:
    def __init__(self, sprite, _game, coord):
        self.sprite = sprite
        self.size = sprite.get_size()
        self.game = _game
        self.rect = sprite.get_rect()
        self.set_coord(coord)
        self.rect[0] = self.screen_coord[0]
        self.rect[1] = self.screen_coord[1]

    def set_coord(self, coord):
        self.coord = coord
        self.screen_coord = (board_coord[0] + (self.coord[1] + 0.5) * square.get_size()[0] - self.size[0]/2,\
                        board_coord[1] + (self.coord[0] + 0.5) * square.get_size()[0] - self.size[1]/2)

    # returns whether or not the piece was clicked
    def clicked(self, m_pos):
        mouse_x = m_pos[0]
        mouse_y = m_pos[1]
        mouse_in_x = mouse_x >= self.screen_coord[0] and mouse_x <= self.screen_coord[0] + self.size[0]
        mouse_in_y = mouse_y >= self.screen_coord[1] and mouse_y <= self.screen_coord[1] + self.size[1]
        return mouse_in_x and mouse_in_y

    def show_board(self):
        for row in self.game.board:
            for piece in row:
                print(piece.mtype, end=" ") if isinstance(piece, Piece) else print(0, end =" ")
            print()

# class for location options a piece can move to
class Option(Content):
    def __init__(self, _game, coord, piece):
        Content.__init__(self, option_sprite, _game, coord)
        self.piece = piece

#Piece class is the parent class for all the chess pieces
class Piece(Content):
    mtype = "NA"
    def __init__(self, sprite, side, _game, coord = (0,0)):
        Content.__init__(self, sprite, _game, coord)
        self.side = side
    
    def changeSide(self, side):
        self.side = side

    # to move
    def move(self, coord):
        target = self.game.board[coord[0]][coord[1]]
        if isinstance(target, Piece) and target.side != self.side:
            self.game.black.remove(target) if self.side == "W" else self.game.white.remove(target)
            self.game.board[coord[0]][coord[1]] = 0
        self.game.swap(self.coord, coord)
        self.set_coord(coord)

    def show_option(self):
        pass

    def outOfBound(self, coord):
        return coord[0] < 0 or coord[1] < 0 or coord[0] >= 8 or coord[1] >= 8

    # returns true if the coordinate is occupied by the piece of same side
    def Occupied(self, coord):
        target = self.game.board[coord[0]][coord[1]]
        return isinstance(target, Piece) and target.side == self.side

class Pawn(Piece):
    mtype = "P"
    def __init__(self, side, _game, sprite=pawn_sprite):
        if side == "W":
            sprite = white_pawn_sprite
        Piece.__init__(self, sprite, side, _game)
        self.first_move = True  # is this pawn's next move its first move?
        self.en_passant = False  # can this pawn be en_passant'ed?
    
    def copy(self):
        return Pawn(self.side, self.game)

    def changeSide(self, side):
        Piece.changeSide(self, side)
        self.sprite = pawn_sprite if self.side == "B" else white_pawn_sprite

    def show_option(self):
        direction = 1 if self.side == "B" else -1 
        # if already at the end, option cannot be set
        if self.coord[0] + direction < 0 or self.coord[0] + direction >= 8:
            return

        option_coord = []

        # look for straightly-movable locations
        for i in (1,2):
            coord = (self.coord[0] + direction * i, self.coord[1])
            if self.outOfBound(coord):
                break
            if self.first_move and i == 2 or i == 1:
                target = self.game.board[coord[0]][coord[1]]
                if isinstance(target, Piece):
                    break
                option_coord.append(coord)

        # check for attackable enemies
        for v_dir in (-1,1):
            # check if the vertical coordinates are within the bound
            if self.coord[1] + v_dir >= 0 and self.coord[1] + v_dir < 8:
                enemy = self.game.board[self.coord[0] + direction][self.coord[1] + v_dir]
                if isinstance(enemy, Piece) and enemy.side != self.side:
                    option_coord.append((enemy.coord))
                # DO EN PASSANT
                enemy = self.game.board[self.coord[0]][self.coord[1] + v_dir]
                if isinstance(enemy, Pawn) and enemy.side != self.side and enemy.en_passant:
                    option_coord.append((enemy.coord[0] + direction,enemy.coord[1], enemy))


        # append to the options
        for coord in option_coord:
            self.game.options.append(Option(self.game, coord, self)) 

    def move(self, coord):
        Piece.move(self, coord)
        if self.first_move:
            self.first_move = False
            self.en_passant = True
        elif self.en_passant:
            self.en_passant = False

class Knight(Piece):
    mtype = "N"
    def __init__(self, side, _game, sprite=knight_sprite):
        Piece.__init__(self, sprite, side, _game)
    
    def copy(self):
        return Knight(self.side, self.game)

    def changeSide(self, side):
        Piece.changeSide(self, side)
        self.sprite = knight_sprite if self.side == "B" else white_knight_sprite

    def show_option(self):
        for x_delta in (-2, -1, 1, 2):
            for y_delta in (-2, -1, 1, 2):
                coord = (self.coord[0] + y_delta, self.coord[1] + x_delta)
                if abs(x_delta * y_delta) == 2 and not self.outOfBound(coord):
                    if self.Occupied((coord)):
                        continue
                    self.game.options.append(Option(self.game, coord, self))

class Queen(Piece):
    mtype = "Q"
    def __init__(self, side, _game, sprite=queen_sprite):
        Piece.__init__(self, sprite, side, _game)

    def copy(self):
        return Queen(self.side, self.game)

    def changeSide(self, side):
        Piece.changeSide(self, side)
        self.sprite = queen_sprite if self.side == "B" else white_queen_sprite

    def show_option(self):
        directions = []
        for i in (-1,0,1):
            for j in (-1,0,1):
                if (i,j) != (0,0):
                    directions.append((i,j))
        
        for _dir in directions:
            for dis in range(1,8):
                coord = ( self.coord[0] + _dir[0] * dis, self.coord[1] + _dir[1] * dis )
                # either out of bound or occupied by the same side piece
                if self.outOfBound(coord) or self.Occupied(coord):
                    break
                # if occupied by white piece(the same side case already taken care of)
                if isinstance(self.game.board[coord[0]][coord[1]], Piece):
                    self.game.options.append(Option(self.game, coord, self))
                    break
                self.game.options.append(Option(self.game, coord, self))

class King(Piece):
    mtype = "K"
    def __init__(self, side, _game, sprite=king_sprite):
        Piece.__init__(self, sprite, side, _game)

    def copy(self):
        return King(self.side, self.game)

    def changeSide(self, side):
        Piece.changeSide(self, side)
        self.sprite = king_sprite if self.side == "B" else white_king_sprite

    def show_option(self):
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                coord = (self.coord[0] + i, self.coord[1] + j)
                if self.outOfBound(coord) or (i,j) == (0,0) or self.Occupied(coord):
                    continue
                self.game.options.append(Option(self.game, coord, self))

class Rook(Piece):
    mtype = "R"
    def __init__(self, side, _game, sprite=rook_sprite):
        Piece.__init__(self, sprite, side, _game)

    def copy(self):
        return Rook(self.side, self.game)
    
    def changeSide(self, side):
        Piece.changeSide(self, side)
        self.sprite = rook_sprite if self.side == "B" else white_rook_sprite

    def show_option(self):
        directions = []
        for i in (-1,0,1):
            for j in (-1,0,1):
                if abs(i) != abs(j):
                    directions.append((i,j))
        
        for _dir in directions:
            for dis in range(1,8):
                coord = ( self.coord[0] + _dir[0] * dis, self.coord[1] + _dir[1] * dis )
                # either out of bound or occupied by the same side piece
                if self.outOfBound(coord) or self.Occupied(coord):
                    break
                # if occupied by white piece(the same side case already taken care of)
                if isinstance(self.game.board[coord[0]][coord[1]], Piece):
                    self.game.options.append(Option(self.game, coord, self))
                    break
                self.game.options.append(Option(self.game, coord, self))

class Bishop(Piece):
    mtype = "B"
    def __init__(self, side, _game, sprite=bishop_sprite):
        Piece.__init__(self, sprite, side, _game)

    def copy(self):
        return Bishop(self.side, self.game)
    
    def changeSide(self, side):
        Piece.changeSide(self, side)
        self.sprite = bishop_sprite if self.side == "B" else white_bishop_sprite

    def show_option(self):
        directions = []
        for i in (-1,0,1):
            for j in (-1,0,1):
                if abs(i) == abs(j):
                    directions.append((i,j))
        
        for _dir in directions:
            for dis in range(1,8):
                coord = ( self.coord[0] + _dir[0] * dis, self.coord[1] + _dir[1] * dis )
                # either out of bound or occupied by the same side piece
                if self.outOfBound(coord) or self.Occupied(coord):
                    break
                # if occupied by white piece(the same side case already taken care of)
                if isinstance(self.game.board[coord[0]][coord[1]], Piece):
                    self.game.options.append(Option(self.game, coord, self))
                    break
                self.game.options.append(Option(self.game, coord, self))
