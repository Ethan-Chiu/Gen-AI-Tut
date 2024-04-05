from .player import Player
from .message import HistoryMessage

class Match:
    def __init__(self, match_id, name, players, history_msgs):
        self.id = match_id
        self.name = name
        self.players = players
        self.history_msgs = history_msgs

    @classmethod
    def from_json(cls, json_data):
        match_id = json_data.get('id')
        name = json_data.get('name')
        players = [Player.from_json(player_data) for player_data in json_data.get('players', [])]
        history_msgs = [HistoryMessage.from_json(msg_data) for msg_data in json_data.get('historyMsgs', [])]
        return cls(match_id, name, players, history_msgs)

    def __str__(self):
        return f"Match ID: {self.id}, Name: {self.name}, Players: {self.players}, History Messages: {self.history_msgs}"
