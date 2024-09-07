import pygame

class InGameMenu:
    def __init__(self, window, menu_config=None):
        self.window = window
        self.font = pygame.font.Font(None, 74)
        self.game = None
        self.menu_items = [
            ('Continue', self.continue_game),
            ('Save', self.save_game),
            ('Options', self.show_options),
            ('Main Menu', self.return_to_main_menu),
            ('Quit', self.quit_game)
        ]
        self.menu_running = False
        self.menu_config = menu_config

    def set_game_instance(self, game):
        self.game = game

    def display_menu(self):
        self.menu_running = True
        while self.menu_running:
            self.window.screen.fill(self.menu_config.bgc)
            if self.menu_config.bg_image_path:
                background_image = pygame.image.load(self.menu_config.bg_image_path)
                self.window.screen.blit(background_image, (0, 0))

            self.render_menu_items()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_running = False
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_event(event)

            pygame.display.flip()

    def render_menu_items(self):
        total_items_height = len(self.menu_items) * 100
        start_y = (self.window.height - total_items_height) // 2

        for index, (text, _) in enumerate(self.menu_items):
            menu_text = self.font.render(text, True, (255, 255, 255))
            menu_rect = menu_text.get_rect(center=(self.window.width // 2, start_y + index * 100))
            self.window.screen.blit(menu_text, menu_rect)

    def handle_mouse_event(self, event):
        total_items_height = len(self.menu_items) * 100
        start_y = (self.window.height - total_items_height) // 2

        for index, (_, action) in enumerate(self.menu_items):
            menu_rect = pygame.Rect(
                (self.window.width // 2 - 100, start_y + index * 100 - 50),
                (200, 100)
            )
            if menu_rect.collidepoint(event.pos):
                action()

    def continue_game(self):
        self.menu_running = False

    def save_game(self):
        self.game.save_game()

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



    def return_to_main_menu(self):
        self.menu_running = False
        try:
            from starcrusher2025_games.configs.menu import Menu
        except:
            from configs.menu import Menu
        menu = Menu(self.window, self.menu_config)
        self.game.stop()
        menu.display_menu() 

    def quit_game(self):
        pygame.quit()
        quit()
