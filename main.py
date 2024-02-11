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
        self.score_rect = pygame.Rect(0, 0, 0, 0)

    def display_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_keyboard_rect.collidepoint(event.pos):
                    self.initParty(2, Device.KEYBOARD)
                    return 1
                elif self.play_mouse_rect.collidepoint(event.pos):
                    self.initParty(2, Device.MOUSE)

                    return 1
                elif self.quit_rect.collidepoint(event.pos):
                    return -1

        play_keyboard_text = self.font.render("-> Play with Keyboard", True, (255, 255, 255))
        self.screen.blit(play_keyboard_text, (100, 100))
        self.play_keyboard_rect = play_keyboard_text.get_rect(topleft=(100, 100))

        play_mouse_text = self.font.render("-> Play with Mouse", True, (255, 255, 255))
        self.screen.blit(play_mouse_text, (100, 150))
        self.play_mouse_rect = play_mouse_text.get_rect(topleft=(100, 150))

        quit_text = self.font.render("-> Quit", True, (255, 255, 255))
        self.screen.blit(quit_text, (100, 200))
        self.quit_rect = quit_text.get_rect(topleft=(100, 200))

        return 0
    def display_end_page(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_to_menu_rect.collidepoint(event.pos):
                    return 0

        score_text = self.font.render(f"Party ended with score = {self.party.player.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (100, 100))
        self.score_rect = score_text.get_rect(topleft=(100, 100))

        back_to_menu_text = self.font.render(f"-> Back to menu", True, (255, 255, 255))
        self.screen.blit(back_to_menu_text, (100, 150))
        self.back_to_menu_rect = back_to_menu_text.get_rect(topleft=(100, 150))

        return 2
    def initParty(self, level, device):
        if  self.party == None or self.party.running == False:
            self.party = Party(level, device, 60)

    def main(self):
        while self.running:
            tick = self.clock.tick(60)

            self.screen.fill("#7CC1AC")

            if self.current_page == 0:
                self.current_page =  self.display_menu()
            elif self.current_page == 1:
                party_running, party_player = self.party.play(tick)

                if not party_running:
                    print("Go to end")
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
