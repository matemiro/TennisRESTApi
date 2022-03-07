from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileDetailsSerializer


class ProfileDetails(generics.GenericAPIView):

    serializer_class = ProfileDetailsSerializer

    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, pk=profile_id)
        serializer = self.serializer_class(instance=profile)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

