import pygame
import random
from Game.Player import Player
from Game.Trap import Trap
from Game.Food import Food
from Enums.Devices import Device

class Party:
    def __init__(self, level, device, timer):
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.level = level
        self.Device = device

        self.timer = timer
        self.font = pygame.font.SysFont(None, 36)

        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)

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
                elif event.type == self.timer_event:
                    self.timer -= 1

            self.screen.fill("purple")

            self.drawItems()

            self.onInput()

            self.onBorder()

            self.check_collision_with_foods()

            self.check_collision_with_traps()

            self.drawUi()

            pygame.display.flip()

            self.dt = self.clock.tick(60) / 1000

            if self.timer <= 0:
                self.running = False

        pygame.quit()

    def onInput(self):
        keys = pygame.key.get_pressed()

        if self.Device == Device.MOUSE:
            mouse_pos = pygame.mouse.get_pos()
            direction = pygame.Vector2(mouse_pos[0] - self.player.position.x, mouse_pos[1] - self.player.position.y)

            if direction.length() > 0:
                direction.normalize_ip()

            displacement = direction * self.player.speed * self.dt
            self.player.position += displacement

        elif self.Device == Device.KEYBOARD:
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

        if keys[pygame.K_ESCAPE]:
            self.running = False

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

            if item is self.player:
                text_width, text_height = self.font.size(format(self.player.score))
                text_position = (self.player.position.x - text_width / 2, self.player.position.y - text_height / 2)
                self.printText(format(self.player.score), (255, 255, 255), text_position)

    def generateRandItems(self):
        traps_count = 0
        food_count = 0

        if self.level == 2:
            traps_count, food_count = 2, 5
        elif self.level == 3:
            traps_count, food_count = 3, 3
        elif self.level == 4:
            traps_count, food_count = 4, 2

        self.generateXFood(food_count)

        self.generateXTrap(traps_count)

    def generateXFood(self, count):
        for i in range(count):
            size = 20
            food_position = self.getRandPosition(size, self.foods + self.traps)
            food = Food("yellow", size, food_position)
            self.foods.append(food)

    def generateXTrap(self, count):
        for i in range(count):
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
                if existing_position.position.distance_to(position) < (existing_position.size + size) / 2 + ray_exclusion:
                    collision = True
                    break

            # Verifie les collisions avec les zones d'exclusion autour des objets
            for existing_position in existing_positions:
                if existing_position.position.distance_to(position) < ((existing_position.size + size) / 2 + ray_exclusion):
                    collision = True
                    break

            if not collision:
                return position

    def check_collision_with_foods(self):
        for food in self.foods:
            if self.player.position.distance_to(food.position) < self.player.size + food.size:

                self.player.addScore(1)
                self.player.addSpeed(100)
                self.player.addSize(2)

                self.foods.remove(food)
                self.generateXFood(1)

    def check_collision_with_traps(self):
        for trap in self.traps:
            if self.player.position.distance_to(trap.position) < (self.player.size + trap.size) and self.player.size > trap.size:
                self.player.size /= self.level

                self.traps.remove(trap)
                self.generateXTrap(1)

    def getRandX(self, size):
        return random.randint(size // 1.6, self.screen.get_width() - size // 1.6)

    def getRandY(self, size):
        return random.randint(size // 1.6, self.screen.get_height() - size // 1.6)

    def drawUi(self):
        self.printText("Timer: {}".format(self.timer), (255, 255, 255), (10, 10))
        self.printText("Speed: {}".format(self.player.speed), (255, 255, 255), (10, 40))
        self.printText("Dificulty: {}".format(self.level), (255, 255, 255), (10, 70))

    def printText(self, text, color, position):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=position)
        self.screen.blit(text_surface, text_rect)
