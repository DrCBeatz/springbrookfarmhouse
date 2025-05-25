# accounts/tests/test_accounts.py

import pytest
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_create_user():
    User = get_user_model()
    user = User.objects.create_user(
        username="test",
        email="test@email.com",
        password="testpassword123",
    )
    assert user.username == "test"
    assert user.email == "test@email.com"
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser

@pytest.mark.django_db
def test_create_superuser():
    User = get_user_model()
    admin_user = User.objects.create_superuser(
        username="admin",
        email="admin@email.com",
        password="adminpassword123",
    )
    assert admin_user.username == "admin"
    assert admin_user.email == "admin@email.com"
    assert admin_user.is_active
    assert admin_user.is_staff
    assert admin_user.is_superuser