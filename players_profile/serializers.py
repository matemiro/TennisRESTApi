from django.db.models import Q
from rest_framework import serializers

from games.models import Game
from .models import Profile


class ProfileDetailsSerializer(serializers.ModelSerializer):

    games_played = serializers.SerializerMethodField()
    games_won = serializers.SerializerMethodField()
    games_lost = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user', )

    def get_games_played(self, profile):
        return Game.objects.filter(
            Q(first_player=profile) | Q(second_player=profile)).filter(score__isnull=False).count()

    def get_games_won(self, profile):
        return Game.objects.filter(
            Q(first_player=profile, score__first_player_sets_won=2) |
            Q(second_player=profile, score__second_player_sets_won=2)).count()

    def get_games_lost(self, profile):
        return Game.objects.filter(
            Q(second_player=profile, score__first_player_sets_won=2) |
            Q(first_player=profile, score__second_player_sets_won=2)).count()
