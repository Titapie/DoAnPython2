class Settings():
    """A class to store all settings for Alien Invasion."""
    
    def __init__(self):
        """Initialize the game's settings."""
       # Cài đặt màn hình
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        # cài đặt phi thuyền
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        
        # Cài đặt Bullet
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        
        # cài đặt allien
        self.fleet_drop_speed = 10
        
        # Trò chơi tăng tốc nhanh như thế nào
        self.speedup_scale = 1.1
        # Giá trị điểm của người ngoài hành tinh tăng nhanh như thế nào
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        
        #hướng hạm đội 1 biểu thị bên phải; -1 biểu thị bên trái.
        self.fleet_direction = 1
        
        # Ghi điểm
        self.alien_points = 50
    
    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        