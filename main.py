import pygame
from Game.Party import Party
from Enums.Devices import Device

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        self.current_page = 0
        self.running = True
        self.party = None

        self.play_keyboard_rect = pygame.Rect(0, 0, 0, 0)
        self.play_mouse_rect = pygame.Rect(0, 0, 0, 0)
        self.quit_rect = pygame.Rect(0, 0, 0, 0)
        self.back_to_menu_rect = pygame.Rect(0, 0, 0, 0)

        self.level2_rect = pygame.Rect(0, 0, 0, 0)
        self.level3_rect = pygame.Rect(0, 0, 0, 0)
        self.level4_rect = pygame.Rect(0, 0, 0, 0)

        self.selected_level = 2

    def display_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return -1
                elif event.key == pygame.K_p:
                    # Si la touche 'p' est pressée, initialiser en mode clavier
                    self.initParty(self.selected_level, Device.KEYBOARD)
                    return 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_keyboard_rect.collidepoint(event.pos):
                    self.initParty(self.selected_level, Device.KEYBOARD)
                    return 1
                elif self.play_mouse_rect.collidepoint(event.pos):
                    self.initParty(self.selected_level, Device.MOUSE)
                    return 1
                elif self.level2_rect.collidepoint(event.pos):
                    self.selected_level = 2
                elif self.level3_rect.collidepoint(event.pos):
                    self.selected_level = 3
                elif self.level4_rect.collidepoint(event.pos):
                    self.selected_level = 4
                elif self.quit_rect.collidepoint(event.pos):
                    return -1

        mt = 180
        mr = 280

        title_text = self.font.render("MazBazPyo", True, (255, 255, 255))
        self.screen.blit(title_text, (330 + mr, 50 + mt))

        play_keyboard_text = self.font.render("-> Play with Keyboard", True, (255, 255, 255))
        self.screen.blit(play_keyboard_text, (100 + mr, 100 + mt))
        self.play_keyboard_rect = play_keyboard_text.get_rect(topleft=(100 + mr, 100 + mt))

        play_mouse_text = self.font.render("-> Play with Mouse", True, (255, 255, 255))
        self.screen.blit(play_mouse_text, (100 + mr, 150 + mt))
        self.play_mouse_rect = play_mouse_text.get_rect(topleft=(100 + mr, 150 + mt))

        quit_text = self.font.render("-> Quit", True, (255, 255, 255))
        self.screen.blit(quit_text, (100 + mr, 200 + mt))
        self.quit_rect = quit_text.get_rect(topleft=(100 + mr, 200 + mt))

        level2_text = self.font.render("Level 2 (Easy)", True, (255, 255, 255))
        self.screen.blit(level2_text, (500 + mr, 100 + mt))
        self.level2_rect = level2_text.get_rect(topleft=(500 + mr, 100 + mt))
        if self.selected_level == 2:
            pygame.draw.circle(self.screen, "#FF686B", (480 + mr, 112 + mt), 8)

        level3_text = self.font.render("Level 3 (Normal)", True, (255, 255, 255))
        self.screen.blit(level3_text, (500 + mr, 150 + mt))
        self.level3_rect = level3_text.get_rect(topleft=(500 + mr, 150 + mt))
        if self.selected_level == 3:
            pygame.draw.circle(self.screen, "#FF686B", (480 + mr, 162 + mt), 8)

        level4_text = self.font.render("Level 4 (Hard)", True, (255, 255, 255))
        self.screen.blit(level4_text, (500 + mr, 200 + mt))
        self.level4_rect = level4_text.get_rect(topleft=(500 + mr, 200 + mt))
        if self.selected_level == 4:
            pygame.draw.circle(self.screen, "#FF686B",(480 + mr, 212 + mt), 8)

        return 0

    def display_end_page(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_to_menu_rect.collidepoint(event.pos):
                    return 0
        mt = 150
        mr = 470

        score_title = self.font.render(f"Party ended !", True, (255, 255, 255))
        self.screen.blit(score_title, (100 + mr, 100 + mt))

        score_text = self.font.render(f"Score : {self.party.player.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (100 + mr, 150 + mt))

        back_to_menu_text = self.font.render(f"-> Back to menu", True, (255, 255, 255))
        self.screen.blit(back_to_menu_text, (80 + mr, 230 + mt))
        self.back_to_menu_rect = back_to_menu_text.get_rect(topleft=(80 + mr, 230 + mt))

        return 2

    def initParty(self, level, device):
        if  self.party is None or self.party.running is False:
            self.party = Party(level, device, 60)

    def main(self):
        while self.running:
            tick = self.clock.tick(60)

            self.screen.fill("#7CC1AC")

            if self.current_page == 0:
                self.current_page = self.display_menu()
            elif self.current_page == 1:
                party_running, party_player = self.party.play(tick)

                if not party_running:
                    self.current_page = 2

            elif self.current_page == 2:
                self.current_page = self.display_end_page()

            elif self.current_page == -1:
                self.running = False

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.main()
