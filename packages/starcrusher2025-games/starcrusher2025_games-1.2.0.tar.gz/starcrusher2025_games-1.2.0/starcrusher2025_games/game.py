import pygame
import json
from pathlib import Path

if __name__ == "__main__":
    from configs.player import Player
    from configs.window import Window
    from configs.GameObject import GameObject
    from configs.menu import Menu
    from configs.ingame_menu import InGameMenu
    from configs.menu_config import MenuConfig
    from extra_module import notify_user_if_update_available
else:
    from starcrusher2025_games.configs.player import Player
    from starcrusher2025_games.configs.window import Window
    from starcrusher2025_games.configs.GameObject import GameObject
    from starcrusher2025_games.configs.menu import Menu
    from starcrusher2025_games.configs.ingame_menu import InGameMenu
    from starcrusher2025_games.configs.menu_config import MenuConfig
    from starcrusher2025_games.extra_module import notify_user_if_update_available

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = False
        self._window = Window()
        self._player = Player()
        self._menu_config = MenuConfig()
        self.menu = Menu(self._window, self._menu_config)
        self.menu.set_game_instance(self)
        self.ingame_menu = InGameMenu(self._window, self._menu_config)
        self.ingame_menu.set_game_instance(self)
        self.keys = {
            'left': False,
            'right': False,
            'up': False,
            'down': False
        }
        self.paintmode = False
        self.target_fps = 60
        self.objects = []
        saves_dir = Path('./saves')
        saves_dir.mkdir(parents=True, exist_ok=True)
        self.save_file = './saves/game_save.json'
        notify_user_if_update_available('starcrusher2025-games')
        
        

    def start(self):
        self.running = True
        self.menu.display_menu()
        if not self.menu.menu_running:
            #self.reset_game_state()
            self.game_loop()

    def game_loop(self):
        self.save_parameters()
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

                if event.type == pygame.KEYDOWN:
                    mods = pygame.key.get_mods()
                    if event.key == pygame.K_ESCAPE:
                        self.ingame_menu.display_menu()
                        if not self.ingame_menu.menu_running:
                            #self.reset_game_state()
                            pass
                    elif event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                        self.save_game()
                    elif event.key in [pygame.K_a, pygame.K_LEFT]:
                        self.keys['left'] = True
                    elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                        self.keys['right'] = True
                    elif event.key in [pygame.K_w, pygame.K_UP]:
                        self.keys['up'] = True
                    elif event.key in [pygame.K_s, pygame.K_DOWN]:
                        self.keys['down'] = True
                    elif event.key == pygame.K_F11:
                        self.window.toggle_fullscreen()

                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_a, pygame.K_LEFT]:
                        self.keys['left'] = False
                    elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                        self.keys['right'] = False
                    elif event.key in [pygame.K_w, pygame.K_UP]:
                        self.keys['up'] = False
                    elif event.key in [pygame.K_s, pygame.K_DOWN]:
                        self.keys['down'] = False
                        
            
            self.update()
            self.render()

            self.clock.tick(self.target_fps)

        pygame.quit()
    
    def reset_game_state(self):
        self.running = False
        self.objects.clear()
        self.load_parameters()

    def update(self):
        self.player.handle_keys(self.keys)
        self.player.keep_within_bounds(self.window.width, self.window.height)
        
        for obj in self.objects:
            obj.update()
            obj.keep_within_bounds(self.window.width, self.window.height)
            
            if isinstance(obj, GameObject):
                self.player.handle_collision(obj)

    def render(self):
        if self.paintmode == True:
            self.player.render(self.window.screen)
        else:
            if self.window.get_background_image():
                self.window.screen.blit(self.window.get_background_image(), (0, 0))
            else:
                self.window.screen.fill(self.window.background_color)
            self.player.render(self.window.screen)
            for obj in self.objects:
                obj.render(self.window.screen)
        pygame.display.flip()

    def add_object(self, obj):
        self.objects.append(obj)

    def stop(self):
        self.running = False

    def set_fps(self, fps):
        self.target_fps = fps

    def paint_mode(self,mode):
        if mode == True:
            self.paintmode = True

    def add_object(self, obj):
        self.objects.append(obj)
    
    def save_game(self):
        game_state = {
            'objects': [obj.to_dict() for obj in self.objects]
        }

        try:
            with open(self.save_file, 'w') as file:
                json.dump(game_state, file, indent=4)
            print(f"Game saved successfully to {self.save_file}")
        except IOError as e:
            print(f"Failed to save game: {e}") 

    def load_game(self):
        if Path(self.save_file).is_file():
            with open(self.save_file, 'r') as file:
                game_state = json.load(file)

            self.objects.clear()
            for obj_data in game_state['objects']:
                obj = GameObject.from_dict(obj_data)
                self.objects.append(obj)

            print(f"Game loaded successfully from {self.save_file}")
        else:
            print(f"No save file found at {self.save_file}")

    def save_parameters(self):
        self.save_parameter_file = './saves/game_parameter_save.json'
        self.render()
        pygame.display.flip()
        game_state = {
            'objects': [obj.to_dict() for obj in self.objects]
        }

        try:
            with open(self.save_parameter_file, 'w') as file:
                json.dump(game_state, file, indent=4)
            print(f"Game parameters saved successfully to {self.save_parameter_file}")
        except IOError as e:
            print(f"Failed to save game parameters: {e}")

    def load_parameters(self):
        if Path(self.save_parameter_file).is_file():
            with open(self.save_parameter_file, 'r') as file:
                game_state = json.load(file)

            self.objects.clear()
            for obj_data in game_state['objects']:
                obj = GameObject.from_dict(obj_data)
                self.objects.append(obj)

            print(f"Game parameters loaded successfully from {self.save_parameter_file}")
        else:
            print(f"No parameter save file found at {self.save_parameter_file}")

    @property
    def window(self):
        return self._window

    @property
    def player(self):
        return self._player
    
    @property
    def obj(self):
        return GameObject
    
    @property
    def menu_config(self):
        return self._menu_config

if __name__ == "__main__":
    game = Game()

    game.window.set_size(1000,800)
    game.window.set_bgc(0,0,0)

    game.player.set_color(255,255,255)
    game.player.set_size(10,10)
    game.player.set_speed(5)
    game.player.set_start_pos(400,300)
    
    game.set_fps(60)

    obj1 = game.obj(start_pos=(100, 100), size=(50, 50), color=(255, 0, 0), speed=1)
    obj2 = game.obj(start_pos=(200, 200), size=(75, 75), speed=-0.1, color=(0, 255, 0))

    game.add_object(obj1)
    game.add_object(obj2)

    game.menu_config.set_title("Haha")
    game.menu_config.set_background_color(30,30,30)

    game.start()