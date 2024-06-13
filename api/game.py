import time
from .server import Server
from .manager import Manager
from .models import MatchInfo

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
        print("All matches:")
        matches = self.manager.get_match_list()
        for match in matches:
            print(match)

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

            time.sleep(5)

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

