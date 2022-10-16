"""Profile serializer."""

from rest_framework import serializers

from users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    class Meta:
        """Meta class."""

        model = Profile
        fields = ("picture", "biography")
