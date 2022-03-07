from django.urls import path
from . import views

urlpatterns = [
    path("", views.LeagueCreateListView.as_view(), name="leagues"),
    path("<int:league_id>/", views.LeagueDetailView.as_view(), name="league_detail"),
    path("<int:league_id>/join/", views.JoinLeague.as_view(), name="join_league"),
    path("<int:league_id>/leave/", views.LeaveLeague.as_view(), name="leave_league"),
    path("<int:league_id>/start/", views.StartLeague.as_view(), name="start_league"),
    path("<int:league_id>/end/", views.EndLeague.as_view(), name="end_league"),
]
