class Player:
    def __init__(self, name, score, size, position,  speed):
        self.name = name
        self.score = score
        self.size = size
        self.speed = speed
        self.position = position

    def addScore(self, score):
        self.score += score