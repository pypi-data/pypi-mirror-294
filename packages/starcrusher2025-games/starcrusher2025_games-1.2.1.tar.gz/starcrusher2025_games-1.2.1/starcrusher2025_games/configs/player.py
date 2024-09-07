import pygame
from .GameObject import GameObject

class Player:
    def __init__(self, start_pos=(400, 300), size=(50, 50), speed=5, color=(255, 0, 0), image_path=None):
        self.position = list(start_pos)
        self.start_pos = start_pos
        self.size = size
        self.speed = speed
        self.color = color
        self.image = None

        if image_path:
            self.load_image(image_path)
    
    def player_parameter_save(self):
        self.player_parameter = {
            "start_pos": self.start_pos,
            "size": self.size,
            "speed": self.speed,
            "color": self.color,
            "image": self.image
        }
        return self.player_parameter

    def load_image(self, image_path):
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, self.size)
        except pygame.error as e:
            print(f"Unable to load image at {image_path}: {e}")
            self.image = None

    def handle_keys(self, keys):
        if keys['left']:
            self.position[0] -= self.speed
        if keys['right']:
            self.position[0] += self.speed
        if keys['up']:
            self.position[1] -= self.speed
        if keys['down']:
            self.position[1] += self.speed

    def render(self, screen):
        if self.image:
            screen.blit(self.image, self.position)
        else:
            pygame.draw.rect(screen, self.color, (*self.position, *self.size))

    def keep_within_bounds(self, screen_width, screen_height):
        self.position[0] = max(0, min(self.position[0], screen_width - self.size[0]))
        self.position[1] = max(0, min(self.position[1], screen_height - self.size[1]))

    def set_start_pos(self, x,y):
        self.start_pos = (x,y)
        self.position = list(self.start_pos)

    def set_size(self, width,height):
        self.size = (width, height)
        if self.image:
            self.image = pygame.transform.scale(self.image, self.size)

    def set_speed(self, speed):
        self.speed = speed

    def set_color(self, r,g,b):
        try:
            r = int(r)
            g = int(g)
            b = int(b)

            if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                self.color = (r, g, b)
            else:
                print("RGB values must be between 0 and 255.")
        except ValueError:
            print("Invalid RGB values. Please provide integers.")

    def set_player_image(self, image_path):
        self.load_image(image_path)

    def get_player_position(self):
        return tuple(self.position)

    def handle_collision(self, other_object):
        if isinstance(other_object, GameObject):
            rect_self = pygame.Rect(self.position, self.size)
            rect_other = pygame.Rect(other_object.position, other_object.size)

            if rect_self.colliderect(rect_other):
                overlap_x = rect_self.clip(rect_other).width
                overlap_y = rect_self.clip(rect_other).height

                if overlap_x < overlap_y:
                    if self.position[0] < other_object.position[0]:
                        self.position[0] -= overlap_x
                    else:
                        self.position[0] += overlap_x
                else:
                    if self.position[1] < other_object.position[1]:
                        self.position[1] -= overlap_y
                    else:
                        self.position[1] += overlap_y

    @classmethod
    def create(cls, start_pos=(400, 300), size=(50, 50), speed=5, color=(255, 0, 0), image_path=None):
        return cls(start_pos=start_pos, size=size, speed=speed, color=color, image_path=image_path)
