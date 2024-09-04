class MenuConfig:

    def __init__(self):
        self.title = "My Game"
        self.bgc = (0, 0, 0)
        self.bg_image_path = None

    def set_title(self, title):
        self.title = title

    def set_background_color(self, r, g, b):
        self.bgc = (r, g, b)

    def set_bg_image(self, image_path):
        self.bg_image_path = image_path

    