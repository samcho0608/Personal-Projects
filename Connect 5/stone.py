import os, pygame

current_path = os.path.dirname(__file__)    # returns the current address of the file
image_path = os.path.join(current_path, "images")   # returns the address of images folder

class Stone:
    images = [pygame.transform.scale(pygame.image.load(os.path.join(image_path, i)),(40,40)) for i in ["black_stone.png", "white_stone.png"]]    
    def __init__(self, side, x = 0, y = 0):
        self.side = side        # sets side; True == Black, False == White
        self.set_coord(x,y)     # sets coordinate
        self.image = Stone.images[0 if side else 1]     # sets image based on the side

    def set_coord(self,x, y):
        self.x = x
        self.y = y