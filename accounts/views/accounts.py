"""Accounts views."""

from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from accounts.models import Account
from accounts.permissions import IsAccountOwner
from accounts.serializers import AccountModelSerializer, CreateAccountModelSerializer
from transactions.models import Transaction
from transactions.serializers import TransactionModelSerializer


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
    search_fields = ("type", "name")
    ordering = ("-balance", "-name")
    filter_fields = ("type", "name")

    def get_serializer_class(self):
        """Assign serializer based on action"""
        if self.action in ["create"]:
            return CreateAccountModelSerializer
        else:
            return AccountModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ["create"]:
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAccountOwner, IsAuthenticated]

        return [p() for p in permissions]

    def retrieve(self, request, *args, **kwargs):
        """Get account by id"""
        response = super(AccountViewSet, self).retrieve(request, *args, **kwargs)
        transactions = Transaction.objects.filter(account=self.get_object())

        data = {
            "account": response.data,
            "transactions": TransactionModelSerializer(transactions, many=True).data,
        }
        response.data = data
        return response
