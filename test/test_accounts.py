import pytest
from accounts.models import accounts

def test_account_creation():
    accounts = accounts.objects.create_profile(
        user = 'sadsad',
        name = 'Checking',
        type = 'Bank',
        balance = 0

    )
    assert accounts.user == 'sadsad'