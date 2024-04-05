class HistoryMessage:
    def __init__(self, message_id, match_id, text, user_id, created_at):
        self.message_id = message_id
        self.match_id = match_id
        self.text = text
        self.user_id = user_id
        self.created_at = created_at

    @classmethod
    def from_json(cls, json_data):
        message_id = json_data.get('id')
        match_id = json_data.get('matchId')
        text = json_data.get('text')
        user_id = json_data.get('userId')
        created_at = json_data.get('createAt')
        return cls(message_id, match_id, text, user_id, created_at)

    def __str__(self):
        return f"Message ID: {self.message_id}, Match ID: {self.match_id}, Text: {self.text}, User ID: {self.user_id}, Created At: {self.created_at}"
