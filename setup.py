import random

import prompts


def generate_roles(number_of_players):
    roles = []
    if number_of_players == 5:
        roles = ["Liberal"] * 3 + ["Fascist"] * 1 + ["Hitler"] * 1
    elif number_of_players == 6:
        roles = ["Liberal"] * 4 + ["Fascist"] * 1 + ["Hitler"] * 1
    elif number_of_players == 7:
        roles = ["Liberal"] * 4 + ["Fascist"] * 2 + ["Hitler"] * 1
    elif number_of_players == 8:
        roles = ["Liberal"] * 5 + ["Fascist"] * 2 + ["Hitler"] * 1
    elif number_of_players == 9:
        roles = ["Liberal"] * 5 + ["Fascist"] * 3 + ["Hitler"] * 1
    elif number_of_players == 10:
        roles = ["Liberal"] * 6 + ["Fascist"] * 3 + ["Hitler"] * 1
    random.shuffle(roles)

    return roles


def populate_main_prompt(num_players, name, role):
    prompt = prompts.MAIN_PROMPT.replace("[INSERT NUMBER OF PLAYERS HERE]", num_players)
    prompt = prompt.replace("[INSERT NAME HERE]", name)
    prompt = prompt.replace("[INSERT ROLE HERE]", role)
    prompt = prompt.replace("[INSERT PARTY HERE]", "Liberal" if role == "Liberal" else "Fascist")
    if num_players == 5:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", 3)
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", 1)
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_5_6_PLAYERS)
    elif num_players == 6:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", 4)
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", 1)
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_5_6_PLAYERS)
    elif num_players == 7:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", 4)
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", 2)
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_7_8_PLAYERS)
    elif num_players == 8:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", 5)
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", 2)
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_7_8_PLAYERS)
    elif num_players == 9:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", 5)
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", 3)
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_9_10_PLAYERS)
    elif num_players == 10:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", 6)
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", 3)
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_9_10_PLAYERS)

    return prompt
