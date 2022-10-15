"""Transactions permissions."""

from rest_framework.permissions import BasePermission

from transactions.models import Transaction


class IsTransactionsOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_object_permission(self, request, view, obj: Transaction):
        """Check obj and user are the same."""
        return request.user == obj.account.user
