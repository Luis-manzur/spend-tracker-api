"""Profile serializer."""

from rest_framework import serializers

from users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("picture", "biography", "membership")
