"""The home page of the example portal, in a browser."""

import pytest


@pytest.mark.e2e
class TestHomePageInABrowser:
    def test_loads(self, live_server, page):
        response = page.goto(live_server.url)
        assert response is not None
        assert response.status == 200
