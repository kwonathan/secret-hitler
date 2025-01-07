import random

import prompts


def generate_roles(number_of_players):
    roles = []
    if number_of_players == 5:
        roles = ["a Liberal"] * 3 + ["a Fascist"] * 1 + ["Hitler"] * 1
    elif number_of_players == 6:
        roles = ["a Liberal"] * 4 + ["a Fascist"] * 1 + ["Hitler"] * 1
    elif number_of_players == 7:
        roles = ["a Liberal"] * 4 + ["a Fascist"] * 2 + ["Hitler"] * 1
    elif number_of_players == 8:
        roles = ["a Liberal"] * 5 + ["a Fascist"] * 2 + ["Hitler"] * 1
    elif number_of_players == 9:
        roles = ["a Liberal"] * 5 + ["a Fascist"] * 3 + ["Hitler"] * 1
    elif number_of_players == 10:
        roles = ["a Liberal"] * 6 + ["a Fascist"] * 3 + ["Hitler"] * 1
    random.shuffle(roles)

    return roles


def populate_main_prompt(players, player):
    num_players = len(players)
    prompt = prompts.MAIN_PROMPT.replace("[INSERT NUMBER OF PLAYERS HERE]", str(num_players))
    player_names = ", ".join([player.name for player in players[:-1]]) + f", and {players[-1].name}"
    prompt = prompt.replace("[INSERT PLAYER NAMES HERE]", player_names)
    prompt = prompt.replace("[INSERT NAME HERE]", player.name)
    prompt = prompt.replace("[INSERT ROLE HERE]", player.role)
    prompt = prompt.replace("[INSERT PARTY HERE]", "Liberal" if player.role == "Liberal" else "Fascist")
    if num_players == 5:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", str(3))
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", str(1))
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_5_6_PLAYERS)
    elif num_players == 6:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", str(4))
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", str(1))
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_5_6_PLAYERS)
    elif num_players == 7:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", str(4))
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", str(2))
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_7_8_PLAYERS)
    elif num_players == 8:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", str(5))
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", str(2))
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_7_8_PLAYERS)
    elif num_players == 9:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", str(5))
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", str(3))
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_9_10_PLAYERS)
    elif num_players == 10:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", str(6))
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", str(3))
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_9_10_PLAYERS)

    return prompt
