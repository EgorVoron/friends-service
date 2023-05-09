from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import FriendshipRequest

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user

    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "password"
        )


class FriendshipRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = (
            "id",
            "from_id",
            "to_id"
        )


class UserNoPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            "id",
            "username"
        )
