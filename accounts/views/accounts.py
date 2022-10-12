"""Users views."""

# Django REST Framework
from rest_framework import mixins, viewsets
# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
# Permissions
from rest_framework.permissions import IsAuthenticated

# Models
from accounts.models import Account
from accounts.permissions import IsAccountOwner
# Serializers
from accounts.serializers import AccountModelSerializer, CreateAccountModelSerializer


class AccountViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Account view set.
    Handle Account create, update and retrieve.
    """
    queryset = Account.objects.all()
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ('type', 'name')
    ordering = ('-balance', '-name')
    filter_fields = ('type', 'name')

    def get_serializer_class(self):
        """Assign serializer based on action"""
        if self.action in ["create"]:
            return CreateAccountModelSerializer
        else:
            return AccountModelSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAccountOwner, IsAuthenticated]

        return [p() for p in permissions]
