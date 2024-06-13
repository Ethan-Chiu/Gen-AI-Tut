import time
from .server import Server
from .manager import Manager
from .models import MatchInfo
from datetime import timezone, datetime, timedelta

def validate_chain(multi_prompt_chain,memory):
    try:
        response = multi_prompt_chain.invoke({"input":"test"})
    except Exception as e:
        print("Can't invoke multi_prompt_chain")
        print(f"Error: {e}")
        return False
    try:
        history = memory.load_memory_variables
    except Exception as e:
        print("Can't load memory")
        print(f"Error: {e}")
        return False
    return True


def time_ago(last_time):
    if last_time is None:
        return None
    now = datetime.now(timezone.utc)
    delta = now - last_time
    return delta

class Game:
    def __init__(self, server: Server, chain, memory):
        self.server: Server = server
        self.manager = Manager(server)
        self.chain = chain
        self.memory = memory

    def set_username(self, name):
        self.server.set_username(name)

    def join_match(self):
        res = self.server.join_match()
        if res is None:
            return 
        print(res.get("message"))
        
        try: 
            # Wait for the match to start
            while True:
                time.sleep(5)
                found = self.select_match()
                if found:
                    break
        except Exception as e:
            print(f"Error: {e}")
            self.server.cancel_match()

        # Start the game
        self.start()
            
    def cancel_match(self):
        res = self.server.cancel_match()
        print(f"Match cancelled {res}")

    def select_match(self):
        matches = self.manager.get_match_list()
        # print("All matches:")
        # for match in matches:
        #     print(match)

        on_going_matches = [ match for match in matches if match.match_status == "START"]
        if len(on_going_matches) == 0:
            print("No on going matches, waiting...")
            return False

        current_match_id = on_going_matches[0].id
        if len(on_going_matches) != 1:
            current_match_id = input("Enter the ID of the match you want to join: ")
        print(f"Enter match: (ID: {current_match_id})")
        self.manager.set_current_match(current_match_id)
        return True


    def start(self):

        local_progress = 0
        self.memory.clear()

        info = self.manager.get_match_info()
        print(info)
        print("Topic:", info.topic.description)
        print("Match:", info.name)
        first = info.is_first
        print("Your turn first" if first else "Opponent's turn first")

        userId = self.server.get_user().get("id")
        opponentId = [player.player_id for player in info.players if player.player_id != userId]
        if len(opponentId) != 1:
            print(f"Error: Opponent count: {len(opponentId)}")
            return
        opponentId = opponentId[0]
        print("Opponent ID:", opponentId)

        last_time_opp_respond = None

        while True:
            match = self.manager.get_current_match()

            # Sync with server
            game_progress = len(match.history_msgs)
            while local_progress < game_progress:
                new_messages = match.history_msgs[local_progress]
                print(new_messages.text)

                instruction = self.manager.get_inst(local_progress)
                if instruction is None:
                    print("Stop game: Failed to get instruction.")
                    return
                
                current_input = {"input": instruction}
                self.memory.save_context(current_input, {"output": new_messages.text})
                local_progress += 1

            if local_progress == 4:
                break

            # Get opponent last response time
            # Initialize opponent last response time
            if last_time_opp_respond is None:
                last_time_opp_respond = datetime.now(timezone.utc)

            last_time = None
            time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
            for message in match.history_msgs:
                if message.user_id == opponentId:
                    message_time = datetime.strptime(message.created_at, time_format)
                    message_time = message_time.replace(tzinfo=timezone.utc)
                    if last_time is None or message_time > last_time:
                        last_time = message_time
            if last_time is not None:
                last_time_opp_respond = last_time
            
            delta = time_ago(last_time_opp_respond)
            print(f"Opponent respond {delta} seconds ago")
            if delta > timedelta(seconds=90):
                print("The last opponent message was more than 90 seconds ago.")
                self.server.overtime()
                return
            
            # Respond 
            my_turn = (first and local_progress % 2 == 0) or (not first and local_progress % 2 == 1)
            
            if my_turn:
                # respond
                instruction = self.manager.get_inst(local_progress)
                if instruction is None:
                    print("Stop game: Failed to get instruction.")
                    return
                
                current_input = {"input": instruction}
                print("current_input", current_input)
                response = self.chain.invoke(current_input)
                answer = response.get("answer")

                # save
                print(answer)
                self.memory.save_context(current_input, {"output": answer})
                local_progress += 1

                # push
                self.manager.send_message(answer)

            if local_progress == 4:
                break

            time.sleep(10)

        self.manager.end_match()
        print("Match over")


def show_result(server: Server):
    manager = Manager(server)
    userId = server.get_user().get("id")
    user_matches = manager.get_match_list()
    for match in user_matches:
        if match.match_status == "GRADED":
            print(f"Your match {match.name} is graded")
            match_info_data = server.get_match_info(match.id)
            match_info = MatchInfo.from_json(match_info_data)
            result = match_info.result
            winnerId = result.winnerId
            
            if (winnerId == userId):
                print(f"You win!")
            else:
                print("You lose!")
            
            for point in result.points:
                if point.userId == userId:
                    print(f"You got {point.point} point")
                    break

            print("\n\nGrading info:")
            print(match_info.result.comment)
            print("-" * 80 + "\n\n")

