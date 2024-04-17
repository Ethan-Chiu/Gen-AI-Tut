class Result:
    def __init__(self, id, winner_id: int, comment:str, match_id: int):
        self.id = id
        self.winnerId = winner_id
        self.comment = comment
        self.matchId = match_id

    @classmethod
    def from_json(cls, json_data):
        id = json_data.get('id')
        winnerId = json_data.get('winnerId')
        comment = json_data.get('comment')
        matchId = json_data.get('matchId')

        return cls(id, winnerId, comment, matchId)

    def __str__(self):
        return f"Result ID: {self.id}, winner ID: {self.winnerId}, comment: {self.comment}, Match ID: {self.matchId}"
