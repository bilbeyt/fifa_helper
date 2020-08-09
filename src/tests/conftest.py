"""Pytest configuration module"""
import pytest
from werkzeug.test import Client
from src.app import App


@pytest.fixture
def client():
    """Fixture client required to test endpoints"""
    return Client(App())
