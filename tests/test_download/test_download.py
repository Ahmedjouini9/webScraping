import pytest
from unittest.mock import patch, Mock
from MyProject.src.modules.download.firefox import Download


@pytest.fixture
def mock_firefox():
    with patch("selenium.webdriver.Firefox") as mock_firefox:
        yield mock_firefox


@pytest.fixture
def mock_firefox_profile():
    with patch("selenium.webdriver.FirefoxProfile") as mock_firefox_profile:
        yield mock_firefox_profile


def test_fetch_data(mock_firefox):
    download_instance = Download()

    mock_driver = mock_firefox.return_value

    mock_driver.find_element.return_value = Mock()

    with patch("time.sleep") as mock_sleep:
        mock_sleep.side_effect = lambda x: None

        download_instance.fetch_data("Some Institution")

        mock_driver.get.assert_called_once_with(
            "https://anabin.kmk.org/no_cache/filter/institutionen.html"
        )
        mock_driver.find_element.assert_called_with(
            "xpath", '//*[@id="searchTabs"]/ul/li[2]'
        )
        mock_driver.save_screenshot.assert_called_once_with("screenshot.png")


def test_main(mocker):
    mock_fetch_data = mocker.patch(
        "MyProject.src.modules.download.firefox.Download.fetch_data"
    )

    Download.main()

    mock_fetch_data.assert_called_once_with("Ecole de l'Aviation de Borj El Amri")
