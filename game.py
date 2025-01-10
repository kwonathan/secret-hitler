import random

class Game:
    def __init__(self, players):
        self.players = players
        self.policy_deck = random.shuffle(["Liberal"] * 6 + ["Fascist"] * 11)
        if len(self.players) == 5 or len(self.players) == 6:
            self.fascist_track = "5_6"
        elif len(self.players) == 7 or len(self.players) == 8:
            self.fascist_track = "7_8"
        else:
            self.fascist_track = "9_10"

        self.president = None
        self.chancellor = None
        self.president_index = 0
        self.election_tracker = 0
        self.nominated_president = None

        self.liberal_policies = 0
        self.fascist_policies = 0
        self.draw_pile = self.policy_deck
        self.discard_pile = []

        self.hitler_dead = False
        self.hitler_elected = False
        self.five_liberal_policies_enacted = False
        self.six_fascist_policies_enacted = False

        self.message_history = []
        self.game_state = None

    def generate_game_state(self):
        current_game_state = ""
        if self.game_state is None:
            current_game_state += "The game has just started. There is no previous President or Chancellor.\n"
        current_player_names = ", ".join([player.name for player in self.players])
        current_game_state += f"There are {len(self.players)} players in the game: {current_player_names}.\n"
        current_game_state += f"{self.nominated_president.name} is the current President.\n"
        current_game_state += f"{self.nominated_president.name} is selecting a Chancellor.\n"
        current_game_state += f"The election tracker is at {self.election_tracker}.\n"
        if self.game_state is not None:
            current_game_state += f"The last President was {self.president.name}.\n"
            current_game_state += f"The last Chancellor was {self.chancellor.name}.\n"
        current_game_state += f"There are now {self.liberal_policies} Liberal Policies.\n"
        current_game_state += f"There are now {self.fascist_policies} Fascist Policies."
        self.game_state = current_game_state

    def play_round(self):
        # ELECTION
        while self.chancellor is None:
            # New Presidential Candidate
            self.nominated_president = self.players[self.president_index]
            self.generate_game_state()
            self.message_history.append(f"The current game state is:\n{self.game_state}")

            # Chancellor nomination
            nominated_chancellor = None
            while nominated_chancellor is None:
                message_history = "\n\n".join(self.message_history)
                chancellor, message = self.nominated_president.select_chancellor(message_history)
                self.message_history.append(f"{self.nominated_president.name} says: {message}")
                if chancellor:
                    nominated_chancellor_name = message.split("I nominate ")[1].split(" as Chancellor")[0]
                    for player in self.players:
                        if player.name == nominated_chancellor_name:
                            nominated_chancellor = player
                else:
                    for player in self.players:
                        if player.name != self.nominated_president.name:
                            message_history = "\n\n".join(self.message_history)
                            message = player.chat(message_history)
                            self.message_history.append(f"{player.name} says: {message}")

            # Voting
            votes = []
            message_history = "\n\n".join(self.message_history)
            for player in self.players:
                vote = player.vote(message_history)
                votes.append(vote)
                self.message_history.append(f"{player.name} votes {vote}")
            if votes.count("Ja!") > votes.count("Nein!"):
                self.election_tracker = 0
                self.president = self.nominated_president
                self.chancellor = nominated_chancellor
                self.message_history.append(f"Majority vote, {self.president.name} becomes the new President and {self.chancellor.name} becomes the new Chancellor.")
                if self.fascist_policies >= 3:
                    if self.chancellor.role == "Hitler":
                        self.hitler_elected = True
                    else:
                        self.message_history.append(f"{self.chancellor.name} is not Hitler.")
            else:
                self.election_tracker += 1
                if self.election_tracker == 3:
                    top_policy = self.draw_pile.pop(0)
                    self.message_history.append(f"Not a majority vote, and the election tracker has moved by 1 to 3. The top Policy in the Policy deck will now be enacted, which is a {top_policy} Policy.")
                    self.election_tracker = 0
                    if top_policy == "Liberal":
                        self.liberal_policies += 1
                        if self.liberal_policies == 5:
                            self.five_liberal_policies_enacted = True
                    else:
                        self.fascist_policies += 1
                        if self.fascist_policies == 6:
                            self.six_fascist_policies_enacted = True
                    if len(self.draw_pile) < 3:
                        new_policy_deck = random.shuffle(self.draw_pile + self.discard_pile)
                        self.draw_pile = new_policy_deck
                        self.discard_pile = []
                else:
                    self.message_history.append(f"Not a majority vote, the election tracker has moved by 1 to {self.election_tracker}. The next player becomes the President.")

            self.president_index += 1
            self.president_index %= len(self.players)

        # Check win condition
        if self.hitler_elected or self.five_liberal_policies_enacted or self.six_fascist_policies_enacted:
            return

        # LEGISLATIVE SESSION
        policy_candidates = self.draw_pile[:3]
        self.draw_pile = self.draw_pile[3:]
        discarded_policy, policy_candidates = self.president.enact_policy(policy_candidates)
        self.discard_pile.append(discarded_policy)
        discarded_policy, enacted_policy = self.chancellor.enact_policy(policy_candidates)
        self.discard_pile.append(discarded_policy)

        if enacted_policy == "Liberal":
            self.liberal_policies += 1
            if self.liberal_policies == 5:
                self.five_liberal_policies_enacted = True
        else:
            self.fascist_policies += 1
            if self.fascist_policies == 6:
                self.six_fascist_policies_enacted = True

        if len(self.draw_pile) < 3:
            new_policy_deck = random.shuffle(self.draw_pile + self.discard_pile)
            self.draw_pile = new_policy_deck
            self.discard_pile = []

        self.message_history.append(f"The President and Chancellor have enacted a {enacted_policy} Policy.")

        # Check win condition
        if self.five_liberal_policies_enacted or self.six_fascist_policies_enacted:
            return

        if enacted_policy == "Liberal":
            return
        if enacted_policy == "Fascist" and self.fascist_track == "5_6" and self.fascist_policies <= 2:
            return
        if enacted_policy == "Fascist" and self.fascist_track == "7_8" and self.fascist_policies == 1:
            return

        # EXECUTIVE ACTION
        # ...

    def check_win_condition(self):
        if self.hitler_elected or self.six_fascist_policies_enacted:
            return True, "Fascists"
        elif self.hitler_dead or self.five_liberal_policies_enacted:
            return True, "Liberals"
        else:
            return False, None
