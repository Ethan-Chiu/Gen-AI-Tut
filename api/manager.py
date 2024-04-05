from .models import Match
from .server import Server

class Manager:
    def __init__(self, server: Server):
        self.server = server
        self.current_match_id = None

    def get_match_list(self):
        matches = self.server.get_user_matches()
        matches = [Match.from_json(match) for match in matches]
        return matches

    def set_current_match(self, match_id):
        self.current_match_id = match_id

    def get_current_match(self) -> Match | None:
        match_data = self.server.get_match(self.current_match_id)
        if match_data:
            match = Match.from_json(match_data)
            return match
        else:
            print("Failed to get current match.")
            return None
        

    def send_message(self, message):
        if self.current_match_id is None:
            print("No current match ID set. Use get_current_match() first.")
            return

        response = self.server.send_message(self.current_match_id, message)
        if response:
            print("Message sent successfully.")
        else:
            print("Failed to send message.")