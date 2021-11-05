# from score import Score

class Ship:

    def __init__(self, size_x, size_y, start_x, start_y):
        self.sunk = False
        self.isHit = False
        self.timeOfHit = 0
        self.size_x = size_x
        self.size_y = size_y
        self.start_x = start_x
        self.start_y = start_y
        self.representOfShip = []

        if size_x == 1 and size_y == 1:
            self.representOfShip.append([start_x, start_y])
        else:
            if size_x < size_y:
                for i in range(start_y, start_y + size_y):
                    self.representOfShip.append([start_x, i])
                    if self.size_x > 1:
                        self.representOfShip.append([start_x + 1, i])
            elif size_x > size_y:
                for i in range(start_x, start_x + size_x):
                    self.representOfShip.append([i, start_y])
                    if self.size_y > 1:
                        self.representOfShip.append([i, start_y + 1])
