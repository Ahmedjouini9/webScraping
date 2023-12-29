import pytest
from unittest.mock import patch, Mock, call
from selenium.webdriver.common.by import By
from MyProject.src.modules.diploma.fetch_data import FetchDiplomaData


@pytest.fixture
def fetch_diploma_data_fixture():
    with patch("MyProject.src.core.web_scraper.WebScraper") as mock_web_scraper, patch(
        "MyProject.src.modules.diploma.data_extractor.DiplomaDataExtractor"
    ) as mock_data_extractor:
        url = "https://anabin.kmk.org/no_cache/filter/hochschulabschluesse.html"
        fetch_diploma_data = FetchDiplomaData(url)
        mock_scraper_instance = mock_web_scraper.return_value
        mock_data_extractor_instance = mock_data_extractor.return_value
        yield fetch_diploma_data, mock_scraper_instance, mock_data_extractor_instance


def test_fetch_data(fetch_diploma_data_fixture):
    (
        fetch_diploma_data,
        mock_scraper_instance,
        mock_data_extractor_instance,
    ) = fetch_diploma_data_fixture

    # Mocking the behavior of the WebScraper
    mock_scraper_instance.open_website.return_value = None
    mock_scraper_instance.click_element.return_value = None
    mock_scraper_instance.select_option_by_value.return_value = None
    mock_scraper_instance.find_elements.return_value = [Mock() for _ in range(5)]

    mock_data_extractor_instance.extract_data.return_value = (
        "University",
        "Location",
        "Program",
        "Degree",
        "Language",
        "Duration",
        "Accreditation",
    )

    # Call the fetch_data method
    fetch_diploma_data.fetch_data()

    # Add assertions based on your expected behavior
    mock_scraper_instance.assert_called_once_with(fetch_diploma_data.url)
    mock_scraper_instance.open_website.assert_called_once()
    mock_scraper_instance.click_element.assert_has_calls(
        [
            call(By.XPATH, '//*[@id="searchTabs"]/ul/li[2]/a'),
            call(By.XPATH, '//*[@id="land-auswaehlen-abschluss"]'),
            call(By.XPATH, '//*[@id="check-land-216"]'),
            call(By.XPATH, '//*[@id="close"]'),
        ]
    )
    mock_scraper_instance.find_elements.assert_called_once_with(
        By.XPATH, '//*[@id="abschlusstabelle"]/tbody/tr'
    )
    mock_data_extractor_instance.extract_data.assert_called()
    mock_scraper_instance.find_element.assert_called_with(
        By.ID, "abschlusstabelle_next"
    )
    mock_scraper_instance.close_website.assert_called_once()

    # Check any state changes or other expected behavior
    assert (
        fetch_diploma_data.information
        == [
            (
                "University",
                "Location",
                "Program",
                "Degree",
                "Language",
                "Duration",
                "Accreditation",
            )
        ]
        * 5
    )


def test_fetch_cell_data_clicks_button(fetch_diploma_data_fixture):
    fetch_diploma_data, mock_scraper_instance, _ = fetch_diploma_data_fixture

    # Mocking the behavior of the WebScraper
    mock_scraper_instance.find_element.return_value = Mock()
    button_element = mock_scraper_instance.find_element.return_value
    button_element.find_elements.return_value = [Mock()]

    # Call the fetch_cell_data method
    fetch_diploma_data.fetch_cell_data(Mock(), mock_scraper_instance)

    # Assert that the button was clicked
    button_element.find_elements.assert_called_once_with(By.TAG_NAME, "img")
    button_element.find_elements.return_value[0].click.assert_called_once()

    # Add more assertions based on expected behavior


def test_fetch_cell_data_handles_no_button(fetch_diploma_data_fixture):
    fetch_diploma_data, mock_scraper_instance, _ = fetch_diploma_data_fixture

    # Mocking the behavior of the WebScraper
    mock_scraper_instance.find_element.return_value = Mock()
    button_element = mock_scraper_instance.find_element.return_value
    button_element.find_elements.return_value = []

    # Call the fetch_cell_data method
    fetch_diploma_data.fetch_cell_data(Mock(), mock_scraper_instance)

    # Assert that the method does not attempt to click the button
    button_element.find_elements.assert_called_once_with(By.TAG_NAME, "img")
    button_element.find_elements.return_value[0].click.assert_not_called()


# Repeat the same pattern for the remaining tests
# ...


if __name__ == "__main__":
    pytest.main()
