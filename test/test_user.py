import pytest
from users.models import Profile

def test_profile_creation():
    profile = Profile.objects.create_profile(
        user = 'dsfsdf',
        picture = ' ',
        biography = 'sfgdfg',

    )
    assert profile.user == 'dsfsdf'