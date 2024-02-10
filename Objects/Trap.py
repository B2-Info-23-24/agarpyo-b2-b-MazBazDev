class Trap:
    def __init__(self, color, size, position):
        self.color = color
        self.size = size
        self.position = position

    def draw(self, pygame, screen):
        pygame.draw.circle(screen, self.color, self.position, self.size)