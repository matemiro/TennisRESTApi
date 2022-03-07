from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileDetailsSerializer


class ProfileDetails(generics.GenericAPIView):

    serializer_class = ProfileDetailsSerializer

    @swagger_auto_schema(operation_summary="Get user's profile details")
    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, pk=profile_id)
        serializer = self.serializer_class(instance=profile)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Update profile details")
    def patch(self, request, profile_id):
        profile = get_object_or_404(Profile, pk=profile_id)
        if not profile.user == request.user:
            return Response(data={"message": "That is not your Profile"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

