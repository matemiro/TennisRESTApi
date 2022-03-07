from .models import User
from rest_framework import serializers


class UserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate(self, data):
        username_exists = User.objects.filter(username=data["username"]).exists()
        if username_exists:
            raise serializers.ValidationError(detail="User with username exists")

        email_exists = User.objects.filter(username=data["email"]).exists()
        if email_exists:
            raise serializers.ValidationError(detail="User with email exists")

        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"]
        )

        user.set_password(validated_data["password"])
        user.save()
        return user
