"""The home page of the example portal."""

import pytest


@pytest.mark.django_db
class TestHomePage:
    def test_answers_a_visitor(self, client):
        assert client.get("/").status_code == 200
