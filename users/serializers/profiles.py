"""Profile serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    class Meta:
        """Meta class."""

        model = Profile
        fields = ("picture", "biography", "balance")
        read_only_fields = ("balance",)
