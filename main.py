import argparse
import random

import game
import player
import setup


if __name__ == "__main__":
    # Determine the number of players
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--players", type=int, choices=[5, 6, 7, 8, 9, 10], default=5, help="specify the number of players")
    parser.add_argument("-H", "--humans", type=int, choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], default=0, help="specify the number of human players")
    parser.add_argument("-S", "--strategy", type=str, choices=["True", "False"], default="False", help="specify whether the AI should use an optional strategy prompt")
    parser.add_argument("-M", "--model", type=str, choices=["gpt-4o", "gpt-4o-mini"], default="gpt-4o-mini", help="specify the model to use for the AI")
    args = parser.parse_args()

    # Initialise game state
    args.humans = min(args.humans, args.players)
    player_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]
    human_player_names = player_names[:args.humans]
    num_players = args.players

    roles = setup.generate_roles(num_players)
    is_human = [True if name in human_player_names else False for name in player_names[:num_players]]
    models = [args.model] * num_players
    players = [player.Player(name, role, human, model) for name, role, human, model in zip(player_names[:num_players], roles, is_human, models)]

    for player in players:
        main_prompt = setup.populate_main_prompt(players, player, args.strategy)
        if player.name in human_player_names:
            print(main_prompt)
            input("[PRESS ENTER TO CONTINUE]")
        player.set_main_prompt(main_prompt)

    random.shuffle(players)

    main_game = game.Game(players)

    # Main game loop
    while True:
        main_game.play_round()
        game_won, winner = main_game.check_win_condition()
        if game_won:
            print(f"The {winner} have won!")
            break
