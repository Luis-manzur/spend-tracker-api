"""Transactions views."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from transactions.models import Transaction
from transactions.permissions import IsTransactionsOwner
from transactions.serializers import (
    CreateTransactionModelSerializer,
    TransactionModelSerializer,
)


class TransactionViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Transaction view set.
    Handle Transactions create, update, delete and retrieve.
    """

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ("type", "name", "category")
    ordering_fields = ("amount", "created", "-created")
    ordering = (
        "-created",
        "amount",
    )
    filter_fields = ("type", "name", "category")

    def get_queryset(self):
        queryset = Transaction.objects.all()
        if self.action == "list":
            queryset = Transaction.objects.filter(
                account__user=self.request.user, monthlybill=None
            )
        return queryset

    def get_serializer_class(self):
        """Assign serializer based on action"""
        if self.action in ["create"]:
            return CreateTransactionModelSerializer
        else:
            return TransactionModelSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            permissions = [IsAuthenticated]
        else:
            permissions = [IsTransactionsOwner, IsAuthenticated]

        return [p() for p in permissions]

    def create(self, request, *args, **kwargs):
        serializer: CreateTransactionModelSerializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.context["user"] = self.request.user
        transaction = serializer.save()
        transaction = TransactionModelSerializer(transaction).data
        headers = self.get_success_headers(transaction)
        return Response(transaction, status=status.HTTP_201_CREATED, headers=headers)
