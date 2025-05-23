class GameStats():
    """Track statistics for Alien Invasion."""
    
    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # Bắt đầu trò chơi ở trạng thái không hoạt động.
        self.game_active = False
        
       # Điểm cao sẽ được đọc từ tệp high_score.txt hoặc đặt thành 0
        try:
            with open('high_score.txt', 'r') as high_score_file:
                self.high_score = int(high_score_file.read())
        except FileNotFoundError:
            self.high_score = 0
    
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        