class GameState():
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.round = '0'
        self.log_list = ['⠀','⠀','⠀',"Fight has started"]
        self.log = '\n'.join(self.log_list)
    def add_log(self, line: str):
        self.log_list.append(line)
        self.log = '\n'.join(self.log_list)
        self.log_list.pop(0)
    def next_round(self):
        self.round = str(int(self.round) + 1)