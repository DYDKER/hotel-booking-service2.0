from django.conf import settings


def test_secret_key():
    assert settings.SECRET_KEY