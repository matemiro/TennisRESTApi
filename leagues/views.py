from itertools import combinations

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from .models import League, LEAGUE_STATUS
from .serializers import LeagueCreationSerializer, LeagueDetailSerializer
from players_profile.models import Profile
from games.models import Game


class LeagueCreateListView(generics.GenericAPIView):

    serializer_class = LeagueCreationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Get list of all leagues")
    def get(self, request):
        leagues = League.objects.all()
        serializer = self.serializer_class(instance=leagues, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Create a league")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeagueDetailView(generics.GenericAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Update league info")
    def patch(self, request, league_id):
        league = get_object_or_404(League, pk=league_id)
        serializer = LeagueCreationSerializer(instance=league, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Get league details")
    def get(self, request, league_id):
        league = get_object_or_404(League, pk=league_id)
        serializer = LeagueDetailSerializer(instance=league)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class JoinLeague(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Join the league")
    def post(self, request, league_id):
        user = get_object_or_404(Profile, user=request.user)
        league = get_object_or_404(League, pk=league_id)

        if not user.is_complete():
            return Response(data={"message": "Incompleted Profile"}, status=status.HTTP_400_BAD_REQUEST)

        if league.status == 'OPEN':
            if user in league.players.all():
                return Response(data={"message": "League already joined"}, status=status.HTTP_400_BAD_REQUEST)

            league.players.add(user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "League is not OPENED"}, status=status.HTTP_400_BAD_REQUEST)


class LeaveLeague(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Leave the league")
    def post(self, request, league_id):
        user = get_object_or_404(Profile, user=request.user)
        league = get_object_or_404(League, pk=league_id)

        if league.status == 'OPEN':
            if user not in league.players.all():
                return Response(data={"message": "League does not joined"}, status=status.HTTP_400_BAD_REQUEST)

            league.players.remove(user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "League is not OPENED"}, status=status.HTTP_400_BAD_REQUEST)


class StartLeague(generics.GenericAPIView):

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="Start the league")
    def post(self, request, league_id):
        league = get_object_or_404(League, pk=league_id)

        if not league.players.count() >= league.min_number_of_players:
            return Response(data={"message": "Not enough players to start the league"},
                            status=status.HTTP_400_BAD_REQUEST)

        if league.status == LEAGUE_STATUS[0][0]:
            league.status = LEAGUE_STATUS[1][0]
            league.save()

            unique_players_pairs = combinations(league.players.all(), 2)
            for first_player, second_player in unique_players_pairs:
                Game(first_player=first_player, second_player=second_player, exhibition=league).save()

            return Response(status=status.HTTP_200_OK)

        return Response(data={"message": f"League can be started only if its status is {LEAGUE_STATUS[0][0]}"},
                        status=status.HTTP_400_BAD_REQUEST)


class EndLeague(generics.GenericAPIView):

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="End the league")
    def post(self, request, league_id):
        league = get_object_or_404(League, pk=league_id)
        league.status = LEAGUE_STATUS[2][0]
        league.save()
        return Response(status=status.HTTP_200_OK)
