class Player:
    def __init__(self, name, color, score, size, position,  speed):
        self.name = name
        self.color = color
        self.score = score
        self.size = size
        self.speed = speed
        self.position = position

    def draw(self, pygame, screen):
        pygame.draw.circle(screen, self.color, self.position, self.size)

    def addScore(self, score):
        self.score += score

    def addSpeed(self, speed):
        if self.speed + speed <= 500:
            self.speed += speed

    def addSize(self, size):
        if self.size + size <= 200:
            self.size += size