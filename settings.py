class Settings:
    def __init__(self):
        self.GRAVITY = 0.75
        self.SCROLL_THRESH = 200
        self.ROWS = 16
        self.COLS = 150
        self.TILE_SIZE = 64
        self.TILE_TYPES = 21
        self.MAX_LEVEL = 2
        self.screen_scroll = 0
        self.bg_scroll = 0
        self.level = 1
        self.start_game = False
        self.start_intro = False
        self.moving_left = False
        self.moving_right = False
        self.shoot = False
        self.grenade = False
        self.grenade_thrown = False

