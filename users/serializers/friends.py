"""Friends Serializers"""
from rest_framework import serializers

from users.models.friends import FriendRequest
from users.serializers import SimpleUserSerializer


class CreateFriendRequestModelSerializer(serializers.Serializer):
    from_user = serializers.SlugRelatedField(
        slug_field="username", read_only=True, many=False
    )
    to_user = serializers.SlugRelatedField(
        slug_field="username", read_only=True, many=False
    )

    def create(self, validated_data):
        data = {
            "from_user": validated_data["from_user"].id,
            "to_user": validated_data["to_user"].id,
        }
        friend_request = FriendRequest.objects.create(**validated_data).save()

        return friend_request


class FriendRequestModelSerializer(serializers.ModelSerializer):
    from_user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ("id", "from_user")


class AcceptFriendRequestSerializer(serializers.Serializer):
    class Meta:
        model = FriendRequest
        fields = ("id",)
