from .player import Player
from .message import HistoryMessage

class Topic:
    def __init__(self, id, description):
        self.id = id
        self.description = description

    @classmethod
    def from_json(cls, json_data):
        id = json_data.get('id')
        description = json_data.get('description')

        return cls(id, description)

    def __str__(self):
        return f"Topic ID: {self.id}, Description: {self.description}"
