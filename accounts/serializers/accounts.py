"""Account serializer."""
from django.core.paginator import Paginator
from rest_framework import serializers

from accounts.models import Account
from accounts.operations import get_transactions_queryset
from spendTrackerApi import settings
from transactions.serializers import TransactionModelSerializer
from utils.operations import get_pagination


class AccountModelSerializer(serializers.ModelSerializer):
    """Account model serializer."""

    class Meta:
        """Meta class."""

        model = Account
        fields = ("name", "type", "balance")
        read_only_fields = ("balance",)


class RetrieveAccountModelSerializer(serializers.ModelSerializer):
    """Retrieve Account model serializer"""

    transactions = serializers.SerializerMethodField("paginated_transactions")

    def paginated_transactions(self, obj):
        request = self.context["request"]
        default_offset = settings.REST_FRAMEWORK["PAGE_SIZE"]
        page_size = int(request.query_params.get("limit") or default_offset)
        transactions = get_transactions_queryset(
            obj.transactions.all(), request.query_params
        )
        paginator = Paginator(transactions, page_size)
        offset = int(request.query_params.get("offset") or 0)

        count, next_page, previous_page, data = get_pagination(
            offset, page_size, paginator, request, transactions
        )
        paginated_transactions = {
            "count": count,
            "next": next_page,
            "previous": previous_page,
            "results": TransactionModelSerializer(data, many=True).data,
        }
        return paginated_transactions

    class Meta:
        """Meta class."""

        model = Account
        fields = ("name", "type", "balance", "transactions")


class CreateAccountModelSerializer(serializers.ModelSerializer):
    """Create account model serializer."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        """Meta class."""

        model = Account
        exclude = ["is_active"]
