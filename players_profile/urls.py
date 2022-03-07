from django.urls import path
from . import views

urlpatterns = [
    path("<int:profile_id>/", views.ProfileDetails.as_view(), name="profile"),
]
