
import pygame

from Objects.Player import Player
from Enums.Devices import Device


class Party:
    def __init__(self, Device=Device):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.Device = Device

        self.player = Player(
            "mazbaz",
            0,
            10,
            pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2),
            0
        )

        self.player_speed = 300

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("purple")

            pygame.draw.circle(self.screen, "red", self.player.position, 40)


            if self.Device == Device.MOUSE :
                mouse_pos = pygame.mouse.get_pos()
                direction = pygame.Vector2(mouse_pos[0] - self.player.position.x, mouse_pos[1] - self.player.position.y)

                if direction.length() > 0:
                    direction.normalize_ip()

                displacement = direction * self.player_speed * self.dt
                self.player.position += displacement

            elif self.Device == PartyType.KEYBOARD:
                keys = pygame.key.get_pressed()
                # up
                if keys[pygame.K_z]:
                    self.player.position.y -= 300 * self.dt
                # down
                if keys[pygame.K_s]:
                    self.player.position.y += 300 * self.dt
                # left
                if keys[pygame.K_q]:
                    self.player.position.x -= 300 * self.dt
                # right
                if keys[pygame.K_d]:
                    self.player.position.x += 300 * self.dt

            # Vérifier si le joueur est sorti de l'écran
            if self.player.position.x < 0:
                self.player.position.x = self.screen.get_width()
            elif self.player.position.x > self.screen.get_width():
                self.player.position.x = 0
            if self.player.position.y < 0:
                self.player.position.y = self.screen.get_height()
            elif self.player.position.y > self.screen.get_height():
                self.player.position.y = 0

            pygame.display.flip()

            self.dt = self.clock.tick(60) / 1000
        pygame.quit()

