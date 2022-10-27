"""Monthly Bill views."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts import models

from transactions.models import MonthlyBill
from transactions.serializers import MonthlyBillModelSerializer


class MonthlyBillsViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
 """Monthly_Bills view set.
    Handle  list and retrieve.
 """
 def get_queryset(self):
        queryset = MonthlyBill.objects.all()
        if self.action == "list":
            queryset = MonthlyBill.objects.filter(account__user=self.request.user)
            queryset = MonthlyBill.objects.filter(MonthlyBill=True)
        return queryset

def get_serializer_class(self):
        """Assign serializer based on action"""
        if self.action in []:
            return MonthlyBill
        else:
            return MonthlyBillModelSerializer
