import random

class Game:
    def __init__(self, players):
        self.players = players
        self.policy_deck = random.shuffle(["Liberal"] * 6 + ["Fascist"] * 11)

        self.president = None
        self.chancellor = None
        self.president_index = 0
        self.election_tracker = 0
        self.last_president = None
        self.last_chancellor = None

        self.liberal_policies = 0
        self.fascist_policies = 0
        self.draw_pile = self.policy_deck
        self.discard_pile = []

        self.hitler_dead = False
        self.hitler_elected = False

        self.message_history = []
        self.game_state = None

    def generate_game_state(self):
        current_game_state = ""
        if self.game_state is None:
            current_game_state += "The game has just started. There is no previous President or Chancellor.\n"
        current_player_names = ", ".join([player.name for player in self.players])
        current_game_state += f"There are {len(self.players)} players in the game: {current_player_names}.\n"
        current_game_state += f"{self.president.name} is the current President.\n"
        current_game_state += f"{self.president.name} is selecting a Chancellor.\n"
        current_game_state += f"The election tracker is at {self.election_tracker}.\n"
        if self.game_state is not None:
            current_game_state += f"The last President was {self.last_president}.\n"
            current_game_state += f"The last Chancellor was {self.last_chancellor}.\n"
        current_game_state += f"There are now {self.liberal_policies} Liberal Policies.\n"
        current_game_state += f"There are now {self.fascist_policies} Fascist Policies."
        self.game_state = current_game_state

    def play_round(self):
        self.president = self.players[self.president_index]
        self.generate_game_state()
        self.message_history.append(f"The current game state is:\n{self.game_state}")

        # ELECTION
        while self.chancellor is None:
            message_history = "\n\n".join(self.message_history)
            chancellor, message = self.president.select_chancellor(message_history)
            self.message_history.append(f"{self.president.name} says: {message}")
            if chancellor:
                self.chancellor = message.split("I nominate ")[1].split(" as Chancellor.")
            else:
                for player in self.players:
                    if player.name != self.president.name:
                        message_history = "\n\n".join(self.message_history)
                        message = player.chat(message_history)
                        self.message_history.append(f"{player.name} says: {message}")
