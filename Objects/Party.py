import pygame
import random

from Objects.Player import Player
from Objects.Trap import Trap
from Objects.Food import Food
from Enums.Devices import Device


class Party:
    def __init__(self, level, device):
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        self.running = True

        self.dt = 0

        self.level = level
        self.Device = device

        self.player = Player(
            "mazbaz",
            "red",
            0,
            40,
            pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2),
            100
        )

        self.traps = []
        self.foods = []

        self.generateRandItems()

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("purple")

            self.drawItems()

            self.onInput()

            self.onBorder()

            pygame.display.flip()

            self.dt = self.clock.tick(60) / 1000
        pygame.quit()

    def onInput(self):
        if self.Device == Device.MOUSE:
            mouse_pos = pygame.mouse.get_pos()
            direction = pygame.Vector2(mouse_pos[0] - self.player.position.x, mouse_pos[1] - self.player.position.y)

            if direction.length() > 0:
                direction.normalize_ip()

            displacement = direction * self.player.speed * self.dt
            self.player.position += displacement

        elif self.Device == Device.KEYBOARD:
            keys = pygame.key.get_pressed()
            # up
            if keys[pygame.K_z]:
                self.player.position.y -= self.player.speed * self.dt
            # down
            if keys[pygame.K_s]:
                self.player.position.y += self.player.speed * self.dt
            # left
            if keys[pygame.K_q]:
                self.player.position.x -= self.player.speed * self.dt
            # right
            if keys[pygame.K_d]:
                self.player.position.x += self.player.speed * self.dt

    def onBorder(self):

        if self.player.position.x < 0:
            self.player.position.x = self.screen.get_width()
        elif self.player.position.x > self.screen.get_width():
            self.player.position.x = 0
        if self.player.position.y < 0:
            self.player.position.y = self.screen.get_height()
        elif self.player.position.y > self.screen.get_height():
            self.player.position.y = 0

    def drawItems(self):
        all_items = self.foods + self.traps + [self.player]
        sorted_items = sorted(all_items, key=lambda item: item.size)

        for item in sorted_items:
            item.draw(pygame, self.screen)

    def generateRandItems(self):
        traps_count = 0
        food_count = 0

        if self.level == 2:
            traps_count, food_count = 2, 5
        elif self.level == 3:
            traps_count, food_count = 3, 3
        elif self.level == 4:
            traps_count, food_count = 4, 2

        for i in range(food_count):
            size = 20
            food_position = self.getRandPosition(size, self.foods + self.traps)
            food = Food("yellow", size, food_position)
            self.foods.append(food)

        for i in range(traps_count):
            size = random.randint(40, 150)
            trap_position = self.getRandPosition(size, self.foods + self.traps)
            trap = Trap("blue", size, trap_position)
            self.traps.append(trap)

    def getRandPosition(self, size, existing_positions):
        ray_exclusion = 20
        while True:
            position = pygame.Vector2(self.getRandX(size), self.getRandY(size))
            collision = False

            # Vérifie les collisions avec les positions existantes
            for existing_position in existing_positions:
                if existing_position.position.distance_to(position) < (existing_position.size + size) / 2:
                    collision = True
                    break

            # Verifie les collisions avec les zones d'exclusion autour des objets
            for existing_position in existing_positions:
                if existing_position.position.distance_to(position) < (
                        existing_position.size + size) / 2 + ray_exclusion:
                    collision = True
                    break

            if not collision:
                return position

    def getRandX(self, size):
        return random.randint(size // 1.6, self.screen.get_width() - size // 1.6)

    def getRandY(self, size):
        return random.randint(size // 1.6, self.screen.get_height() - size // 1.6)

