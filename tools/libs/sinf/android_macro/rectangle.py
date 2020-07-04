class Rectangle:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.center_x = 0
        self.center_y = 0

    def setX(self, x):
        self.x = x
        self.update()

    def setY(self, y):
        self.y = y
        self.update()

    def setW(self, w):
        self.w = w
        self.update()

    def setH(self, h):
        self.h = h
        self.update()

    def update(self):
        self.center_x = self.x + int(self.w/2)
        self.center_y = self.y + int(self.h/ 2)

    def __str__(self):
        return f"pos: ({self.x},{self.y}), size: ({self.w}, {self.h}), center: ({self.center_x}, {self.center_y})"

    def __repr__(self):
        return f"pos: ({self.x},{self.y}), size: ({self.w}, {self.h}), center: ({self.center_x}, {self.center_y})"