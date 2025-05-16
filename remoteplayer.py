class RemotePlayer:
    def __init__(self, screen, player_num, game, addr):
        super().__init__(screen, player_num, game)
        self.addr = addr
