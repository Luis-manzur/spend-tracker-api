"""Debts views."""

from django.db.models import Q
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from debts.models import Debt
from debts.serializers import DebtModelSerializer, CreateDebtModelSerializer, PayDebtModelSerializer


class DebtViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Account view set.
    Handle Account create, update and retrieve.
    """

    filter_backends = (OrderingFilter, SearchFilter)
    filter_fields = ("to_user", "from_user")

    def get_serializer_class(self):
        """Assign serializer based on action"""
        if self.action in ["create"]:
            return CreateDebtModelSerializer
        elif self.action in ["pay_debt"]:
            return PayDebtModelSerializer
        else:
            return DebtModelSerializer

    def get_queryset(self):
        queryset = Debt.objects.all()
        if self.action == "list":
            queryset = Debt.objects.filter(
                Q(from_user=self.request.user) | Q(to_user=self.request.user)
            )
        return queryset

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]

        return [p() for p in permissions]

    @action(detail=False, methods=["post"], url_name="pay")
    def pay_debt(self, request, *args, **kwargs):
        serializer = PayDebtModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        data = {"message": "Debt Paid successfully!"}
        return Response(data, status=status.HTTP_200_OK)
