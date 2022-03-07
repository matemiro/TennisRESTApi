from django.db import models
from django.db.models import F, Q

from players_profile.models import Profile
from leagues.models import League


class Game(models.Model):

    exhibition = models.ForeignKey(League, on_delete=models.SET_NULL, null=True, blank=True, related_name='matches')
    first_player = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='matches_first_player')
    second_player = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='matches_second_player')
    date = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~Q(first_player=F('second_player')),
                name='first_player_and_second_player_can_not_be_equal'),
        ]

    def __str__(self):
        first_player_name = self.first_player.surname if self.first_player else 'Profile deleted'
        second_player_name = self.second_player.surname if self.second_player else 'Profile deleted'
        if hasattr(self, 'score'):
            return f"{first_player_name} {self.score.get_score()} {second_player_name}"
        else:
            return f"{first_player_name} v {second_player_name}"


class Score(models.Model):

    game = models.OneToOneField(Game, on_delete=models.CASCADE, null=True, blank=True, related_name='score')

    first_player_sets_won = models.SmallIntegerField()
    second_player_sets_won = models.SmallIntegerField()

    first_player_games_won_set_1 = models.SmallIntegerField()
    second_player_games_won_set_1 = models.SmallIntegerField()
    first_player_games_won_set_2 = models.SmallIntegerField()
    second_player_games_won_set_2 = models.SmallIntegerField()
    first_player_games_won_set_3 = models.SmallIntegerField(null=True, blank=True)
    second_player_games_won_set_3 = models.SmallIntegerField(null=True, blank=True)

    def get_score(self):
        scores = (
            (self.first_player_games_won_set_1, self.second_player_games_won_set_1),
            (self.first_player_games_won_set_2, self.second_player_games_won_set_2),
            (self.first_player_games_won_set_3, self.second_player_games_won_set_3),
        )
        return ", ".join((f"{first_player_score}/{second_player_score}" for first_player_score, second_player_score
                          in scores if first_player_score is not None and second_player_score is not None))
