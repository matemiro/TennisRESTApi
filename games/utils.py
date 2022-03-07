def get_match_winner_loser_and_sets_result(game):
    if hasattr(game, 'score'):
        if game.score.first_player_sets_won > game.score.second_player_sets_won:
            return game.first_player, game.second_player, game.score.first_player_sets_won, game.score.second_player_sets_won
        else:
            return game.second_player, game.first_player, game.score.second_player_sets_won, game.score.first_player_sets_won
    else:
        return None

