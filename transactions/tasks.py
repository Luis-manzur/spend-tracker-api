import datetime

from celery import shared_task

from transactions.models import MonthlyBill
from transactions.serializers import CreateTransactionModelSerializer


@shared_task()
def apply_monthly_bills():
    """apply all monthly bills from today."""
    date = datetime.date.today().day
    monthly_bills = MonthlyBill.objects.filter(billing_date=date)
    for monthly_bill in monthly_bills:
        transaction = monthly_bill.transaction
        new_transaction = {
            "name": transaction.name,
            "description": transaction.description,
            "amount": transaction.amount,
            "is_month_to_month": False,
            "type": transaction.type,
            "category": transaction.category,
            "account": transaction.account_id
        }
        serializer = CreateTransactionModelSerializer(new_transaction)
        if serializer.is_valid():
            serializer.save()
