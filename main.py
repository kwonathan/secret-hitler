import argparse
import random

import game
import player
import setup


if __name__ == "__main__":
    # Determine the number of players
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--players", type=int, choices=[5, 6, 7, 8, 9, 10], default=5, help="specify the number of players")
    args = parser.parse_args()

    # Initialise game state
    player_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]
    num_players = args.players

    roles = setup.generate_roles(num_players)
    players = [player.Player(name, role) for name, role in zip(player_names[:num_players], roles)]

    for player in players:
        main_prompt = setup.populate_main_prompt(players, player)
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
