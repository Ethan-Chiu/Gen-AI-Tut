class Point:
    def __init__(self, id, user_id: int, result_id: int, point: int):
        self.id = id
        self.userId: int = user_id
        self.resultId = result_id
        self.point = point  

    @classmethod
    def from_json(cls, json_data):
        id = json_data.get('id')
        userId = json_data.get('userId')
        resultId = json_data.get('resultId')
        point = json_data.get('point')

        return cls(id, userId, resultId, point)

    def __str__(self):
        return f"Point ID: {self.id}, User ID: {self.userId}, Result ID: {self.resultId}, Point: {self.point}"
