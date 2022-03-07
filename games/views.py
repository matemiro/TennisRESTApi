import re

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from games.serializers import UserGamesSerializer

from players_profile.models import Profile

from .models import Game, Score
from .serializers import ScoreValidationSerializer
from leagues.models import LEAGUE_STATUS


class UserGames(generics.GenericAPIView):

    serializer_class = UserGamesSerializer

    @swagger_auto_schema(operation_summary="Get list of User's games")
    def get(self, request, user_id):
        user = get_object_or_404(Profile, pk=user_id)
        games = Game.objects.filter(Q(first_player=user) | Q(second_player=user))
        serializer = self.serializer_class(instance=games, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProvideScore(generics.GenericAPIView):

    serializer_class = ScoreValidationSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Provide score")
    def post(self, request, game_id):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            user = get_object_or_404(Profile, user=request.user)
            game = get_object_or_404(Game, pk=game_id)

            if user not in (game.first_player, game.second_player) or not request.user.is_superuser:
                return Response(data={"message": "Only players and administrator can provide result"},
                                status=status.HTTP_400_BAD_REQUEST)

            if league := game.exhibition:
                if not league.status == LEAGUE_STATUS[1][0]:
                    return Response(data={"message": f"League status is not {LEAGUE_STATUS[1][0]}"},
                                    status=status.HTTP_400_BAD_REQUEST)

            if hasattr(game, 'score'):
                return Response(data={"message": "Score already provided"}, status=status.HTTP_400_BAD_REQUEST)

            games = [int(game) for game in re.findall(r'\d', serializer.data.get('score'))]
            first_player_sets_won = sum((1 for val1, val2 in zip(games[0::2], games[1::2]) if val1 > val2))
            second_player_sets_won = sum((1 for val1, val2 in zip(games[0::2], games[1::2]) if val1 < val2))

            Score(
                game=game,
                first_player_sets_won=first_player_sets_won,
                second_player_sets_won=second_player_sets_won,
                first_player_games_won_set_1=games[0],
                second_player_games_won_set_1=games[1],
                first_player_games_won_set_2=games[2],
                second_player_games_won_set_2=games[3],
                first_player_games_won_set_3=games[4] if len(games) == 6 else None,
                second_player_games_won_set_3=games[5] if len(games) == 6 else None
            ).save()

            return Response(status=status.HTTP_200_OK)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameScoreValidation(generics.GenericAPIView):

    serializer_class = ScoreValidationSerializer

    @swagger_auto_schema(operation_summary="Validate score")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
