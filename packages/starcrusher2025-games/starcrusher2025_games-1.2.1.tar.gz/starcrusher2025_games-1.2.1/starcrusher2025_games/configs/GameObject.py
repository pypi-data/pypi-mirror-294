import pygame

class GameObject:
    def __init__(self, start_pos=(0, 0), size=(50, 50), speed=0, color=(255, 255, 255), image_path=None, is_moveable=False):
        self.position = list(start_pos)
        self.start_pos = start_pos
        self.size = size
        self.speed = speed
        self.color = color
        self.image = None
        self.is_moveable = is_moveable

        if image_path:
            self.load_image(image_path)

    def obj_parameter_save(self):
        self.obj_parameter = {
            "start_pos": self.start_pos,
            "size": self.size,
            "speed": self.speed,
            "color": self.color,
            "image": self.image,
            "is_moveable": self.is_moveable
        }
        return self.obj_parameter

    def load_image(self, image_path):
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, self.size)
        except pygame.error as e:
            print(f"Unable to load image at {image_path}: {e}")
            self.image = None

    def render(self, screen):
        if self.image:
            screen.blit(self.image, self.position)
        else:
            pygame.draw.rect(screen, self.color, (*self.position, *self.size))

    def update(self):
        self.position[0] += self.speed

    def handle_collision(self, other_object):
        if isinstance(other_object, GameObject):
            rect_self = pygame.Rect(self.position, self.size)
            rect_other = pygame.Rect(other_object.position, other_object.size)
            
            if rect_self.colliderect(rect_other):
                self.resolve_collision(rect_self, rect_other)

    def resolve_collision(self, rect_self, rect_other):
        overlap_x = rect_self.clip(rect_other).width
        overlap_y = rect_self.clip(rect_other).height
        
        if overlap_x < overlap_y:
            if self.position[0] < rect_other.x:
                self.position[0] -= overlap_x
            else:
                self.position[0] += overlap_x
        else:
            if self.position[1] < rect_other.y:
                self.position[1] -= overlap_y
            else:
                self.position[1] += overlap_y

    def keep_within_bounds(self, screen_width, screen_height):
        self.position[0] = max(0, min(self.position[0], screen_width - self.size[0]))
        self.position[1] = max(0, min(self.position[1], screen_height - self.size[1]))

    def to_dict(self):
        return {
            'position': self.position,
            'size': self.size,
            'speed': self.speed,
            'color': self.color,
            'is_moveable': self.is_moveable
        }

    @classmethod
    def from_dict(cls, obj_dict):
        try:
            return cls(
                start_pos=obj_dict.get('position', (0, 0)),
                size=obj_dict.get('size', (50, 50)),
                speed=obj_dict.get('speed', 0),
                color=obj_dict.get('color', (255, 255, 255))
            )
        except KeyError as e:
            print(f"Error creating GameObject from dictionary: Missing key {e}")
            return None