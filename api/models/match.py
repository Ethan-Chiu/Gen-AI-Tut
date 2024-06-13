from .player import Player
from .message import HistoryMessage
from .topic import Topic
from .result import Result

class Match:
    def __init__(self, match_id, name, topic_id, match_status, players, history_msgs):
        self.id = match_id
        self.name = name
        self.topic_id = topic_id
        self.match_status = match_status
        self.players = players
        self.history_msgs: list[HistoryMessage] = history_msgs

    @classmethod
    def from_json(cls, json_data):
        match_id = json_data.get('id')
        name = json_data.get('name')
        topic_id = json_data.get('topicId')
        match_status = json_data.get('matchStatus')
        players = [Player.from_json(player_data) for player_data in json_data.get('players', [])]
        history_msgs = [HistoryMessage.from_json(msg_data) for msg_data in json_data.get('historyMsgs', [])]
        return cls(match_id, name, topic_id, match_status, players, history_msgs)

    def __str__(self):
        return f"Match ID: {self.id}, Name: {self.name}, Topic ID: {self.topic_id}, Match Status: {self.match_status}, Players: {self.players}, History Messages: {self.history_msgs}"


class MatchInfo:
    def __init__(self, match_id, topic_id, name, players, topic, is_first, result):
        self.id = match_id
        self.name = name
        self.topic_id = topic_id
        self.players: list[Player] = players
        self.topic: Topic = topic
        self.is_first = is_first
        self.result: Result | None = result

    @classmethod
    def from_json(cls, json_data):
        match_id = json_data.get('id')
        name = json_data.get('name')
        topic_id = json_data.get('topicId')
        players = [Player.from_json(player_data) for player_data in json_data.get('players', [])]
        topic = Topic.from_json(json_data.get('topic'))
        is_first = json_data.get('isFirst')
        result = Result.from_json(json_data.get('result')) if json_data.get('result') else None
        return cls(match_id, name, topic_id, players, topic, is_first, result)

    def __str__(self):
        return f"Match ID: {self.id}, Name: {self.name}, Topic ID: {self.topic_id}, Players: {self.players}, Topic: {self.topic}, Is First: {self.is_first}, Result: {self.result}"