import pygame

class Window:
    def __init__(self, width=800, height=600):
        self._width = width
        self._height = height
        self.screen = pygame.display.set_mode((width, height))
        self.background_color = (0, 0, 0)
        self.is_fullscreen = False
        self.background_image = None

    def set_size(self, width, height):
        self._width = width
        self._height = height
        self.screen = pygame.display.set_mode((width, height))

    def set_bgc(self, r, g, b):
        try:
            r = int(r)
            g = int(g)
            b = int(b)

            if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                self.background_color = (r, g, b)
                self.screen.fill(self.background_color)
            else:
                print("RGB values must be between 0 and 255.")
        except ValueError:
            print("Invalid RGB values. Please provide integers.")

    def set_bg_image(self, image_path=None):
        if image_path:
            try:
                self.background_image = pygame.image.load(image_path).convert()
                self.background_image = pygame.transform.scale(self.background_image, (self._width, self._height))
                self.screen.blit(self.background_image, (0, 0))
                pygame.display.update()
            except pygame.error as e:
                print(f"Error loading image: {e}")
                self.screen.fill(self.background_color)
        else:
            self.screen.fill(self.background_color)

    def get_background_image(self):
        return self.background_image

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((self._width, self._height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self._width, self._height))
        self.screen.fill(self.background_color)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
