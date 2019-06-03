class GameManager:
    def __init__(self, game_mode = None):
        self.is_game_over = False
        self.time_played = 0
        self.total_lines_cleared = 0

        self.win_condition = None
        set_game_mode(game_mode)

    def set_game_mode(self, mode):
        if game_mode == 'Marathon':
            self.win_condition = marathon_completed
        elif game_mode == '20l':
            self.win_condition = sprint_20_completed
        elif game_mode == '40l':
            self.win_condition = sprint_40_completed
        elif game_mode == '100l':
            self.win_condition = sprint_100_completed
        elif game_mode == '1000l':
            self.win_condition = sprint_1000_completed

    def marathon_completed(self):
        return self.total_lines_cleared >= 150

    def sprint_20_completed(self):
        return self.total_lines_cleared >= 20

    def sprint_40_completed(self):
        return self.total_lines_cleared >= 40

    def sprint_100_completed(self):
        return self.total_lines_cleared >= 100

    def sprint_1000_completed(self):
        return self.total_lines_cleared >= 1000

    def update_stats(self, lines_cleared = -1, time_spent = -1):
        if lines_cleared > 0:
            self.total_lines_cleared += lines_cleared

        if time_spent >= 0:
            self.time_played += time_spent

    def check_game_over(self):
        return self.win_condition and self.win_condition()
