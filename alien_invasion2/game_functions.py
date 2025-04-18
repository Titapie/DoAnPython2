import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet


def check_keydown_events(event, ai_settings, screen, stats, sb, ship, 
        bullets, aliens):
    """Respond to key presses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, sb, ship, bullets, aliens)
    elif event.key == pygame.K_q:
        stop_game(stats)


def stop_game(stats):
    """Write out the high score and exit the program."""
    with open('high_score.txt', 'w') as high_score_file:
        high_score_file.write(str(stats.high_score))
    sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Tạo một dấu đầu dòng mới và thêm nó vào nhóm dấu đầu dòng.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, 
        aliens, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, 
                bullets, aliens)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, 
                ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
        aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, bullets, aliens)


def start_game(ai_settings, screen, stats, sb, ship, bullets, aliens):
    """Do what's needed to start a new game."""
    # Thiết lập lại cài đặt trò chơi.
    ai_settings.initialize_dynamic_settings()
    
    # Ẩn con trỏ chuột.
    pygame.mouse.set_visible(False)
    
    # Thiết lập lại số liệu thống kê của trò chơi.
    stats.reset_stats()
    stats.game_active = True
    
    # Thiết lập lại hình ảnh bảng điểm.
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    
    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()
    
    # Xóa danh sách người ngoài hành tinh và đạn.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, 
        bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    # Vẽ lại màn hình sau mỗi lần thực hiện vòng lặp.
    screen.fill(ai_settings.bg_color)
    # Vẽ lại tất cả các viên đạn phía sau tàu và người ngoài hành tinh
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    # Vẽ thông tin điểm số
    sb.show_score()    
    
    # Vẽ nút chơi nếu trò chơi không hoạt động
    if not stats.game_active:
        play_button.draw_button()

    # Hiển thị màn hình được vẽ gần đây nhất
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, 
        bullets):
    """Update position of bullets and get rid of old bullets."""
    # Cập nhật vị trí dấu đầu dòng.
    bullets.update()

    # Loại bỏ những viên đạn đã biến mất.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(ai_settings, screen, stats, 
        sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, 
        ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Loại bỏ bất kỳ viên đạn và người ngoài hành tinh nào đã va chạm
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        # Nếu toàn bộ hạm đội bị phá hủy, hãy bắt đầu một cấp độ mới
        bullets.empty()
        ai_settings.increase_speed()
        
        # tăng level
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Tạo một người ngoài hành tinh và tìm số người ngoài hành tinh đứng thành một hàng.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Tạo hàng người ngoài hành tinh đầu tiên.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Giảm ships_left
        stats.ships_left -= 1
        
        # cập nhật bảng điểm
        sb.prep_ships()
        
        # Xóa danh sách người ngoài hành tinh và đạn
        aliens.empty()
        bullets.empty()
        
        # Tạo một hạm đội mới và tập trung tàu vào trung tâm.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
        # tạm dừng
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Xử lý trường hợp này giống như khi tàu bị đâm.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Check if the fleet is at an edge, and then update the positions 
    of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Tìm kiếm va chạm giữa tàu vũ trụ và người ngoài hành tinh
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    
    # Tìm kiếm người ngoài hành tinh đang đâm vào đáy màn hình
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
