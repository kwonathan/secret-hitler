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

def populate_main_prompt(players, player, strategy):
    num_players = len(players)
    prompt = prompts.MAIN_PROMPT.replace("[INSERT NUMBER OF PLAYERS HERE]", str(num_players))
    player_names = ", ".join([player.name for player in players[:-1]]) + f", and {players[-1].name}"
    prompt = prompt.replace("[INSERT PLAYER NAMES HERE]", player_names)
    prompt = prompt.replace("[INSERT NAME HERE]", player.name)
    prompt = prompt.replace("[INSERT ROLE HERE]", player.role)
    prompt = prompt.replace("[INSERT PARTY HERE]", "Liberal" if player.role == "a Liberal" else "Fascist")
    hitler_name = None
    fascist_names = []
    for p in players:
        if p.role == "Hitler":
            hitler_name = p.name
        elif p.role == "a Fascist":
            fascist_names.append(p.name)

    if num_players == 5:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", str(3))
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", str(1))
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_5_6_PLAYERS)
        if player.role == "a Fascist":
            prompt = prompt.replace("[INSERT HITLER/FASCIST INFO HERE]", prompts.FASCIST_PROMPT_5_6_PLAYERS.replace("[INSERT HITLER NAME]", hitler_name))
        elif player.role == "Hitler":
            prompt = prompt.replace("[INSERT HITLER/FASCIST INFO HERE]", prompts.HITLER_PROMPT_5_6_PLAYERS.replace("[INSERT FASCIST NAME]", fascist_names[0]))
        else:
            prompt = prompt.replace("[INSERT HITLER/FASCIST INFO HERE]", "")
    elif num_players == 6:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", str(4))
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", str(1))
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_5_6_PLAYERS)
        if player.role == "a Fascist":
            prompt = prompt.replace("[INSERT HITLER/FASCIST INFO HERE]", prompts.FASCIST_PROMPT_5_6_PLAYERS.replace("[INSERT HITLER NAME]", hitler_name))
        elif player.role == "Hitler":
            prompt = prompt.replace("[INSERT HITLER/FASCIST INFO HERE]", prompts.HITLER_PROMPT_5_6_PLAYERS.replace("[INSERT FASCIST NAME]", fascist_names[0]))
        else:
            prompt = prompt.replace("[INSERT HITLER/FASCIST INFO HERE]", "")
    elif num_players == 7:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", str(4))
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", str(2))
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_7_8_PLAYERS)
        if player.role == "a Fascist":
            prompt = prompt.replace("[INSERT HITLER/FASCIST INFO HERE]", prompts.FASCIST_PROMPT_7_10_PLAYERS.replace("[INSERT FASCIST NAMES]", f"{fascist_names[0]} and {fascist_names[1]}").replace("[INSERT HITLER NAME]", hitler_name))
        else:
            prompt = prompt.replace("[INSERT HITLER/FASCIST INFO HERE]", "")
    elif num_players == 8:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", str(5))
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", str(2))
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_7_8_PLAYERS)
        if player.role == "a Fascist":
            prompt = prompt.replace("[INSERT HITLER/FASCIST INFO HERE]", prompts.FASCIST_PROMPT_7_10_PLAYERS.replace("[INSERT FASCIST NAMES]", f"{fascist_names[0]} and {fascist_names[1]}").replace("[INSERT HITLER NAME]", hitler_name))
        else:
            prompt = prompt.replace("[INSERT HITLER/FASCIST INFO HERE]", "")
    elif num_players == 9:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", str(5))
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", str(3))
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_9_10_PLAYERS)
        if player.role == "a Fascist":
            prompt = prompt.replace("[INSERT HITLER/FASCIST INFO HERE]", prompts.FASCIST_PROMPT_7_10_PLAYERS.replace("[INSERT FASCIST NAMES]", ", ".join(fascist_names[:-1]) + f", and {fascist_names[-1]}").replace("[INSERT HITLER NAME]", hitler_name))
        else:
            prompt = prompt.replace("[INSERT HITLER/FASCIST INFO HERE]", "")
    elif num_players == 10:
        prompt = prompt.replace("[INSERT NUMBER OF LIBERALS]", str(6))
        prompt = prompt.replace("[INSERT NUMBER OF FASCISTS]", str(3))
        prompt = prompt.replace("[INSERT FASCIST TRACK HERE]", prompts.FASCIST_TRACK_9_10_PLAYERS)
        if player.role == "a Fascist":
            prompt = prompt.replace("[INSERT HITLER/FASCIST INFO HERE]", prompts.FASCIST_PROMPT_7_10_PLAYERS.replace("[INSERT FASCIST NAMES]", ", ".join(fascist_names[:-1]) + f", and {fascist_names[-1]}").replace("[INSERT HITLER NAME]", hitler_name))
        else:
            prompt = prompt.replace("[INSERT HITLER/FASCIST INFO HERE]", "")

    if strategy:
        prompt = prompt.replace("[INSERT OPTIONAL STRATEGY PROMPT HERE]", f"\n{prompts.OPTIONAL_STRATEGY_PROMPT}")
    else:
        prompt = prompt.replace("[INSERT OPTIONAL STRATEGY PROMPT HERE]", "")

    return prompt
