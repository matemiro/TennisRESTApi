from django.db import models
from players_profile.models import Profile

from games.utils import get_match_winner_loser_and_sets_result

DEFAULT_MAX_NUMBER_OF_PLAYERS = 20
DEFAULT_MIN_NUMBER_OF_PLAYERS = 4

LEAGUE_STATUS = (
        ("OPEN", "open"),
        ("STARTED", "started"),
        ("ENDED", "ended"),
    )


class League(models.Model):

    name = models.CharField(max_length=40, null=False, blank=False, unique=True)
    description = models.TextField()
    max_number_of_players = models.PositiveSmallIntegerField(default=DEFAULT_MAX_NUMBER_OF_PLAYERS)
    min_number_of_players = models.PositiveSmallIntegerField(default=DEFAULT_MIN_NUMBER_OF_PLAYERS)
    status = models.CharField(choices=LEAGUE_STATUS, max_length=20, default=LEAGUE_STATUS[0][0])
    players = models.ManyToManyField(Profile, related_name='leagues', blank=True)

    def __str__(self):
        return f"{self.name} ({self.max_number_of_players}) - {self.status}"

    def get_table(self):
        if not self.status == LEAGUE_STATUS[0][0]:
            table = {player.id: {'player_name': f"{player.name[0]}. {player.surname}", 'games': 0, 'wins': 0, 'won_sets': 0, 'lost_sets': 0} for player in self.players.all()}
            league_games = self.matches.filter(score__isnull=False) if hasattr(self, 'matches') else []
            for match in league_games:
                winner, loser, winner_sets, loser_sets = get_match_winner_loser_and_sets_result(match)
                table[winner.id]['games'] += 1
                table[loser.id]['games'] += 1

                table[winner.id]['wins'] += 1

                table[winner.id]['won_sets'] += winner_sets
                table[winner.id]['lost_sets'] += loser_sets
                table[loser.id]['won_sets'] += loser_sets
                table[loser.id]['lost_sets'] += winner_sets

            return dict(sorted(table.items(), key=lambda item: (item[1]['wins'], item[1]['won_sets']), reverse=True))

        else:
            return None

