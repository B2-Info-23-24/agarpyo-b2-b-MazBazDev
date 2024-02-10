import pygame
import random

from Objects.Player import Player
from Objects.Trap import Trap
from Objects.Food import Food
from Enums.Devices import Device


class Party:
    def __init__(self, level, device):
        pygame.init()

        self.screen = pygame.display.set_mode((720, 720))
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
        self.player.draw(pygame, self.screen)

        for trap in self.traps:
            trap.draw(pygame, self.screen)

        for food in self.foods:
            food.draw(pygame, self.screen)

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
            food_position = self.getRandPosition(size)
            food = Food("yellow", size, food_position)
            self.foods.append(food)

        for i in range(traps_count):
            size = random.randint(40, 150)
            trap_position = self.getRandPosition(size)
            trap = Trap("blue", size, trap_position)
            self.traps.append(trap)

    def getRandPosition(self, size):
        ray_exclusion = 20
        while True:
            position = pygame.Vector2(self.getRandX(size), self.getRandY(size))
            collision = False

            # Verif les collisions avec les autres pièges
            for trap in self.traps:
                if trap.position.distance_to(position) < (trap.size + size) / 2:
                    collision = True
                    break

            # Verif les collisions avec les autres nourritures
            for food in self.foods:
                if food.position.distance_to(position) < (food.size + size) / 2:
                    collision = True
                    break

            # Verif les collisions avec les zones d'exclusion autour des pièges
            for trap in self.traps:
                if trap.position.distance_to(position) < (trap.size + size) / 2 + ray_exclusion:
                    collision = True
                    break

            # Verif les collisions avec les zones d'exclusion autour des nourritures
            for food in self.foods:
                if food.position.distance_to(position) < (food.size + size) / 2 + ray_exclusion:
                    collision = True
                    break
            if not collision:
                return position
    def sortItemsBySize(self):
        sorted_items = []

    def getRandX(self, size):
        return random.randint(size + 10, self.screen.get_width())

    def getRandY(self, size):
        return random.randint(size + 10, self.screen.get_height())
