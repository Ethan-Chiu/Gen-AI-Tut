class Player:
    def __init__(self, player_id, match_id, created_at):
        self.player_id = player_id
        self.match_id = match_id
        self.created_at = created_at

    @classmethod
    def from_json(cls, json_data):
        player_id = json_data.get('playerId')
        match_id = json_data.get('matchId')
        created_at = json_data.get('createAt')
        return cls(player_id, match_id, created_at)

    def __str__(self):
        return f"Player ID: {self.player_id}, Match ID: {self.match_id}, Created At: {self.created_at}"
