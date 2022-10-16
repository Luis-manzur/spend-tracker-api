"""Monthly bill serializer."""

from rest_framework import serializers

from transactions.models import MonthlyBill


class MonthlyBillModelSerializer(serializers.ModelSerializer):
    """Monthly bill model serializer."""

    class Meta:
        """Meta class."""

        model = MonthlyBill
        fields = ("transaction", "billing_date")
        read_only_fields = ("transaction",)
