import random

class Game:
    def __init__(self, players):
        self.players = players
        self.policy_deck = ["Liberal"] * 6 + ["Fascist"] * 11
        random.shuffle(self.policy_deck)
        if len(self.players) == 5 or len(self.players) == 6:
            self.fascist_track = "5_6"
        elif len(self.players) == 7 or len(self.players) == 8:
            self.fascist_track = "7_8"
        else:
            self.fascist_track = "9_10"
        self.investigated_players = []

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

        self.special_election = False
        self.veto_power = False

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
            if not self.special_election:
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
                        return
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
                            return
                    else:
                        self.fascist_policies += 1
                        if self.fascist_policies == 6:
                            self.six_fascist_policies_enacted = True
                            return
                    if len(self.draw_pile) < 3:
                        new_policy_deck = random.shuffle(self.draw_pile + self.discard_pile)
                        self.draw_pile = new_policy_deck
                        self.discard_pile = []
                else:
                    self.message_history.append(f"Not a majority vote, the election tracker has moved by 1 to {self.election_tracker}. The next player becomes the President.")

            if not self.special_election:
                self.president_index += 1
                self.president_index %= len(self.players)
            self.special_election = False

        # LEGISLATIVE SESSION
        policy_candidates = self.draw_pile[:3]
        self.draw_pile = self.draw_pile[3:]
        message_history = "\n\n".join(self.message_history)
        discarded_policy, policy_candidates = self.president.enact_policy_president(policy_candidates, message_history)
        self.discard_pile.append(discarded_policy)
        if self.veto_power:
            message_history = "\n\n".join(self.message_history)
            veto, discarded_policy, enacted_policy = self.chancellor.enact_policy_veto(policy_candidates, message_history)
            if veto:
                self.message_history.append(f"The Chancellor has requested to veto the Policies.")
                message_history = "\n\n".join(self.message_history)
                if self.president.veto_accepted(message_history):
                    self.discard_pile += policy_candidates
                    self.election_tracker += 1
                    if self.election_tracker == 3:
                        top_policy = self.draw_pile.pop(0)
                        self.message_history.append(f"Veto accepted by the President, and the election tracker has moved by 1 to 3. The top Policy in the Policy deck will now be enacted, which is a {top_policy} Policy.")
                        self.election_tracker = 0
                        if top_policy == "Liberal":
                            self.liberal_policies += 1
                            if self.liberal_policies == 5:
                                self.five_liberal_policies_enacted = True
                                return
                        else:
                            self.fascist_policies += 1
                            if self.fascist_policies == 6:
                                self.six_fascist_policies_enacted = True
                                return
                        if len(self.draw_pile) < 3:
                            new_policy_deck = random.shuffle(self.draw_pile + self.discard_pile)
                            self.draw_pile = new_policy_deck
                            self.discard_pile = []
                    else:
                        self.message_history.append(f"Veto accepted by the President, the election tracker has moved by 1 to {self.election_tracker}. The next player becomes the President.")
                    return
                else:
                    self.message_history.append(f"The President has rejected the veto request.")
                    message_history = "\n\n".join(self.message_history)
                    discarded_policy, enacted_policy = self.chancellor.enact_policy_chancellor(policy_candidates, message_history)
                    self.discard_pile.append(discarded_policy)
            else:
                self.discard_pile.append(discarded_policy)
        else:
            message_history = "\n\n".join(self.message_history)
            discarded_policy, enacted_policy = self.chancellor.enact_policy_chancellor(policy_candidates, message_history)
            self.discard_pile.append(discarded_policy)

        self.message_history.append(f"The President and Chancellor have enacted a {enacted_policy} Policy.")
        message_history = "\n\n".join(self.message_history)
        reveal, message = self.president.reveal_policy(message_history)
        if reveal:
            self.message_history.append(f"{self.president.name} says: {message}")
        message_history = "\n\n".join(self.message_history)
        reveal, message = self.chancellor.reveal_policy(message_history)
        if reveal:
            self.message_history.append(f"{self.chancellor.name} says: {message}")

        if enacted_policy == "Liberal":
            self.liberal_policies += 1
            if self.liberal_policies == 5:
                self.five_liberal_policies_enacted = True
                return
        else:
            self.fascist_policies += 1
            if self.fascist_policies == 6:
                self.six_fascist_policies_enacted = True
                return

        if len(self.draw_pile) < 3:
            new_policy_deck = random.shuffle(self.draw_pile + self.discard_pile)
            self.draw_pile = new_policy_deck
            self.discard_pile = []

        if enacted_policy == "Liberal":
            return
        if enacted_policy == "Fascist" and self.fascist_track == "5_6" and self.fascist_policies <= 2:
            return
        if enacted_policy == "Fascist" and self.fascist_track == "7_8" and self.fascist_policies == 1:
            return

        # EXECUTIVE ACTION
        if self.fascist_track == "7_8" and self.fascist_policies == 2 or self.fascist_track == "9_10" and self.fascist_policies <= 2:
            # Investigate loyalty
            self.message_history.append(f"The newly enacted Fascist Policy allows the President ({self.president.name}) to investigate the loyalty of another player.")
            self.message_history.append(f"There are {len(self.players)} players in the game: {', '.join([player.name for player in self.players])}.")
            self.message_history.append(f"The following players have already been investigated, and cannot be investigated again: {', '.join([player.name for player in self.investigated_players])}.")

            investigated_player = None
            while investigated_player is None:
                message_history = "\n\n".join(self.message_history)
                investigation, message = self.president.investigate_loyalty(message_history)
                self.message_history.append(f"{self.president.name} says: {message}")
                if investigation:
                    investigated_player_name = message.split("I investigate ")[1].split(" for loyalty")[0]
                    for player in self.players:
                        if player.name == investigated_player_name:
                            investigated_player = player
                else:
                    for player in self.players:
                        if player.name != self.president.name:
                            message_history = "\n\n".join(self.message_history)
                            message = player.chat(message_history)
                            self.message_history.append(f"{player.name} says: {message}")

            self.investigated_players.append(investigated_player)
            message_history = "\n\n".join(self.message_history)
            message = self.president.reveal_party_membership(message_history, investigated_player)
            self.message_history.append(f"{self.president.name} has investigated {investigated_player.name} for loyalty. Does the President want to share this information with the group?")
            self.message_history.append(f"{self.president.name} says: {message}")

        elif self.fascist_track == "7_8" and self.fascist_policies == 3 or self.fascist_track == "9_10" and self.fascist_policies == 3:
            # Call Special Election
            self.message_history.append(f"The newly enacted Fascist Policy allows the President ({self.president.name}) to call a Special Election.")
            self.message_history.append(f"There are {len(self.players)} players in the game: {', '.join([player.name for player in self.players])}.")

            special_president = None
            while special_president is None:
                message_history = "\n\n".join(self.message_history)
                special_election, message = self.president.call_special_election(message_history)
                self.message_history.append(f"{self.president.name} says: {message}")
                if special_election:
                    special_president_name = message.split("I nominate ")[1].split(" as President")[0]
                    for player in self.players:
                        if player.name == special_president_name:
                            special_president = player
                else:
                    for player in self.players:
                        if player.name != self.president.name:
                            message_history = "\n\n".join(self.message_history)
                            message = player.chat(message_history)
                            self.message_history.append(f"{player.name} says: {message}")

            self.message_history.append(f"{self.president.name} has called a Special Election. {special_president.name} has been chosen as the new President.")
            self.nominated_president = special_president
            self.special_election = True

        elif self.fascist_track == "5_6" and self.fascist_policies == 3:
            # Policy peek
            self.message_history.append(f"The newly enacted Fascist Policy allows the President ({self.president.name}) to look at the next three Policies in the Policy deck.")
            message_history = "\n\n".join(self.message_history)
            self.president.policy_peek(message_history, self.draw_pile[:3])
            self.message_history.append(f"{self.president.name} has looked at the next three Policies in the Policy deck.")

        else:
            # Execution
            self.message_history.append(f"The newly enacted Fascist Policy allows the President ({self.president.name}) to execute another player.")
            self.message_history.append(f"There are {len(self.players)} players in the game: {', '.join([player.name for player in self.players])}.")

            player_to_be_executed = None
            while player_to_be_executed is None:
                message_history = "\n\n".join(self.message_history)
                execution, message = self.president.execute_player(message_history)
                self.message_history.append(f"{self.president.name} says: {message}")
                if execution:
                    player_to_be_executed_name = message.split("I formally execute ")[1].split(".")[0]
                    for player in self.players:
                        if player.name == player_to_be_executed_name:
                            player_to_be_executed = player
                else:
                    for player in self.players:
                        if player.name != self.president.name:
                            message_history = "\n\n".join(self.message_history)
                            message = player.chat(message_history)
                            self.message_history.append(f"{player.name} says: {message}")

            self.message_history.append(f"{self.president.name} has executed {player_to_be_executed.name}.")
            if player_to_be_executed.role == "Hitler":
                self.hitler_dead = True
                return
            self.players.remove(player_to_be_executed)

            if self.fascist_policies == 5:
                # Veto Power
                self.message_history.append(f"For all subsequent Legislative Sessions, the newly enacted Fascist Policy allows the President and the Chancellor to discard all three Policies in the Policy deck if they both agree.")
                self.veto_power = True

    def check_win_condition(self):
        if self.hitler_elected or self.six_fascist_policies_enacted:
            return True, "Fascists"
        elif self.hitler_dead or self.five_liberal_policies_enacted:
            return True, "Liberals"
        else:
            return False, None
