from django.urls import path
from . import views

urlpatterns = [
    path("user/<int:user_id>/", views.UserGames.as_view(), name="user_games"),
    path("<int:game_id>/", views.ProvideScore.as_view(), name="provide_result"),
    path("score/validation/", views.GameScoreValidation.as_view(), name="score_validation"),
]
