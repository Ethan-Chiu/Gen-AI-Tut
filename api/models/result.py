from .point import Point
from typing import List

class Result:
    def __init__(self, id, winner_id: int, comment:str, match_id: int, points: List[Point]):
        self.id = id
        self.winnerId = winner_id
        self.comment = comment
        self.matchId = match_id
        self.points: List[Point] = points

    @classmethod
    def from_json(cls, json_data):
        id = json_data.get('id')
        winnerId = json_data.get('winnerId')
        comment = json_data.get('comment')
        matchId = json_data.get('matchId')
        points = [Point.from_json(point_data) for point_data in json_data.get('points', [])]
        return cls(id, winnerId, comment, matchId, points)

    def __str__(self):
        return f"Result ID: {self.id}, winner ID: {self.winnerId}, comment: {self.comment}, Match ID: {self.matchId}, Points: {self.points}"
