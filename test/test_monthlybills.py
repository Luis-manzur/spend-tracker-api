import pytest
from transactions.models import monthly_bills

def test_monthlybills_creation():
    monthlybills = monthly_bills.objects.create_profile(
        transactions = 3,
        billing_date = '10-02-2022',

    )
    assert monthlybills.transaction == 3