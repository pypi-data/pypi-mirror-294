from starcrusher2025_games.configs.GameObject import GameObject

class ObjectManager:
    def __init__(self):
        self.objects = []

    def add_obj(self, start_pos, size=(50, 50), speed=0, color=(255, 255, 255), image_path=None, is_moveable=False):
        obj = GameObject(start_pos=start_pos, size=size, speed=speed, color=color, image_path=image_path, is_moveable=is_moveable)
        self.objects.append(obj)

    def update(self, window_width, window_height, player):
        for obj in self.objects:
            obj.update()
            player.handle_collision(obj)
            obj.keep_within_bounds(window_width, window_height)

    def render(self, screen):
        for obj in self.objects:
            obj.render(screen)

    def save_state(self):
        return [obj.obj_parameter_save() for obj in self.objects]

    def load_state(self, objects_data):
        self.objects = [GameObject.from_dict(obj) for obj in objects_data]
