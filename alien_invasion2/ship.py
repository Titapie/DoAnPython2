import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Tải hình ảnh tàu và lấy hình chữ nhật của nó.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # Bắt đầu mỗi tàu mới ở phần giữa phía dưới màn hình.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Lưu trữ giá trị thập phân cho tâm tàu.
        self.center = float(self.rect.centerx)
        
        # Cờ di chuyển
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Update the ship's position based on the movement flag."""
        # Cập nhật giá trị trung tâm của tàu, không phải hình chữ nhật
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        
        # Cập nhật đối tượng hình chữ nhật từ self.center
        self.rect.centerx = self.center
        
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx
        