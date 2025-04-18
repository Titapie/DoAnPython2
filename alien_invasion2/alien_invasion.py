import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

def run_game():
    # Khởi tạo trò chơi và tạo đối tượng màn hình
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")
    
    # Tạo nút Play
    play_button = Button(ai_settings, screen, "Play")
    
    # tạo bảng điểm và nơi lưu trữ số liệu
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    # tạo phi thuyền, đạn và người ngoài hành tinh
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    
    # tạo hạm đội người ngoài hành tinh
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    # bắt đầu vòng lặp chính của game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, 
            aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, 
                aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
    
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, 
            bullets, play_button)

run_game()
