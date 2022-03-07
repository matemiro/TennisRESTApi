import re
import numpy as np

from .models import Game
from rest_framework import serializers


class UserGamesSerializer(serializers.ModelSerializer):

    first_player_name = serializers.SerializerMethodField()
    second_player_name = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    exhibition = serializers.SerializerMethodField()

    class Meta:
        model = Game
        exclude = ["first_player", "second_player"]

    def get_first_player_name(self, obj):
        if obj.first_player.is_complete():
            return f"{obj.first_player.name} {obj.first_player.surname}"
        else:
            return f"Incomplete profile or deleted"

    def get_second_player_name(self, obj):
        if obj.second_player.is_complete():
            return f"{obj.second_player.name} {obj.second_player.surname}"
        else:
            return f"Incomplete profile or deleted"

    def get_score(self, obj):
        return obj.score.get_score() if hasattr(obj, 'score') else None

    def get_exhibition(self, obj):
        if exhibition_name := obj.exhibition:
            return f"{exhibition_name}"
        else:
            return "friendly match"


class ScoreValidationSerializer(serializers.Serializer):

    score = serializers.RegexField(regex=r'^[0-7]\/[0-7] [0-7]\/[0-7] [0-7]\/[0-7]$|^[0-7]\/[0-7] [0-7]\/[0-7]$',
                                   min_length=7, max_length=11, allow_null=False, allow_blank=False)

    def validate_score(self, score):
        sets = re.findall(r'([0-7]\/[0-7])', score)
        sets_scores = [[int(first_player_score), int(second_player_score)]
                       for first_player_score, second_player_score in (set_score.split('/') for set_score in sets)]

        # check if sets sequence is valid (there should not be third set if one player win first two sets)
        sets_sequence = np.sign([score1 - score2 for score1, score2 in sets_scores])
        if sets_sequence[0] == sets_sequence[1] and len(sets_sequence) > 2:
            raise serializers.ValidationError(detail="Wrong sets sequence. If player win first two sets match is ended")
        if not sets_sequence[0] == sets_sequence[1] and len(sets_sequence) == 2:
            raise serializers.ValidationError(detail="Match cannot end with tie")

        # check valid games configuration (e.g. wrong games configurations 6/5, 7/4, 5/2 etc.)
        for idx, set_score in enumerate(sets_scores, start=1):
            loser_score, winner_score = np.sort(set_score)
            if winner_score not in (6, 7):
                raise serializers.ValidationError(detail=f"It takes 6 or 7 games to win a set (set {idx})")

            if loser_score == winner_score:
                raise serializers.ValidationError(detail=f"Number of games cannot be equal (set {idx})")

            if winner_score == 6 and loser_score not in range(5):
                raise serializers.ValidationError(
                    detail=f"If winner won 6 games, than other player should win 0-4 (set {idx})")

            if winner_score == 7 and loser_score not in (5, 6):
                raise serializers.ValidationError(
                    detail=f"If winner won 7 games, than other player should win 5 or 6 (set {idx})")

        return score
