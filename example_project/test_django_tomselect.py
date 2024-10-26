"""Test cases for the django-tomselect package."""

import pytest
from django.conf import settings
from django.utils.translation import gettext as _


def test_succeeds() -> None:
    """Test that the test suite runs."""
    assert 0 == 0


def test_settings() -> None:
    """Test that the settings are configured."""
    assert settings.USE_TZ is True

