from .models import League, DEFAULT_MIN_NUMBER_OF_PLAYERS, DEFAULT_MAX_NUMBER_OF_PLAYERS, LEAGUE_STATUS
from rest_framework import serializers


class LeagueCreationSerializer(serializers.ModelSerializer):

    current_entries = serializers.SerializerMethodField()
    players_joined = serializers.SerializerMethodField()

    class Meta:
        model = League
        exclude = ['players', ]
        read_only_fields = ('status', )

    def get_current_entries(self, league):
        return league.players.count()

    def get_players_joined(self, league):
        return [{player.id: f"{player.name} {player.surname}"} for player in league.players.all()]

    def validate(self, data):
        max_number_of_players = data.get("max_number_of_players") or DEFAULT_MAX_NUMBER_OF_PLAYERS
        min_number_of_players = data.get("min_number_of_players") or DEFAULT_MIN_NUMBER_OF_PLAYERS

        if max_number_of_players < min_number_of_players:
            raise serializers.ValidationError(detail="Max number of players can't be lower than min number of players")

        return data


class LeagueDetailSerializer(LeagueCreationSerializer):

    table = serializers.SerializerMethodField()
    played_matches = serializers.SerializerMethodField()
    matches_not_played = serializers.SerializerMethodField()

    class Meta:
        model = League
        exclude = ('players', )

    def validate_max_number_of_players(self, max_number_of_players):
        if max_number_of_players and max_number_of_players < self.instance.players.count():
            raise serializers.ValidationError(detail="Cannot set max number of players lower than current entries")

        return max_number_of_players

    def get_table(self, league):
        return league.get_table()

    def get_played_matches(self, league):
        return [str(match) for match in league.matches.filter(score__isnull=False)]

    def get_matches_not_played(self, league):
        return [(match.id, str(match)) for match in league.matches.filter(score__isnull=True)]

