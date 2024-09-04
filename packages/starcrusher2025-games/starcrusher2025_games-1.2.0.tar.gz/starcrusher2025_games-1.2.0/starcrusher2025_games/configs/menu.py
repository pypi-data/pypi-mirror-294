import pygame

class Menu:
    def __init__(self, window, menu_config):
        self.window = window
        self.menu_config = menu_config
        self.font = pygame.font.Font(None, 74)
        self.game = None
        self.menu_items = [
            (self.menu_config.title, None),
            ('', None),
            ('Play', self.play_game),
            ('Options', self.show_options),
            ('Load Game', self.load_game),
            ('Quit', self.quit_game)
        ]
        self.menu_running = True

    def set_game_instance(self, game):
        self.game = game

    def display_menu(self):
        try:
            while self.menu_running:
                self.window.screen.fill(self.menu_config.bgc)
                self.render_menu_items()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.menu_running = False
                        self.quit_game()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_mouse_event(event)

                    pygame.display.flip()
        except:
            pass

    def render_menu_items(self):
        for index, (text, _) in enumerate(self.menu_items):
            menu_text = self.font.render(text, True, (255, 255, 255))
            menu_rect = menu_text.get_rect(center=(self.window.width // 2, self.window.height // 2 - 100 + index * 100))
            self.window.screen.blit(menu_text, menu_rect)

    def handle_mouse_event(self, event):
        for index, (_, action) in enumerate(self.menu_items):
            menu_rect = pygame.Rect(
                (self.window.width // 2 - 100, self.window.height // 2 - 100 + index * 100 - 50),
                (200, 100)
            )
            if menu_rect.collidepoint(event.pos):
                try:
                    action()
                except:
                    pass

    def play_game(self):
        self.menu_running = False

    def show_options(self):
        options_running = True
        while options_running:
            self.window.screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 74)
            back_text = font.render('Back', True, (255, 255, 255))
            back_rect = back_text.get_rect(center=(self.window.width // 2, self.window.height // 2))

            self.window.screen.blit(back_text, back_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    options_running = False
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_rect.collidepoint(event.pos):
                        options_running = False

    def load_game(self):
        if self.game:
            self.game.load_game()
            self.menu_running = False
        else:
            print("Game instance not set.")

    def quit_game(self):
        pygame.quit()
        quit()
