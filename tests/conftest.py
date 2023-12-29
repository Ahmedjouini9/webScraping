import pytest
from unittest.mock import Mock, patch


@pytest.fixture
def mock_web_scraper():
    with patch("MyProject.src.core.web_scraper.WebScraper") as mock:
        yield mock.return_value
