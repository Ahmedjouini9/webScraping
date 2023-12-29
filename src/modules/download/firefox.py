import json
import logging
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


class Download:
    def fetch_data(self, institution_name):
        downloadPath = r"c:/users/ahmed/desktop/"
        appState = {
            "recentDestinations": [{"id": "Save as PDF", "origin": "local"}],
            "selectedDestinationId": "Save as PDF",
            "version": 2,
        }
        profile = {
            "printing.print_preview_sticky_settings.appState": json.dumps(appState),
            "browser.download.dir": downloadPath,
            "browser.download.folderList": 2,
            "browser.download.manager.showWhenStarting": False,
            "browser.helperApps.neverAsk.saveToDisk": "application/pdf",
            "print.always_print_silent": True,
            "print.printer_Microsoft_Print_to_PDF.print_to_file": True,
            "print.printer_Microsoft_Print_to_PDF.print_to_filename": f"{institution_name}.pdf",
        }

        firefox_options = FirefoxOptions()
        # Comment out the headless mode for debugging
        # firefox_options.headless = True

        firefox_profile = webdriver.FirefoxProfile()
        for key, value in profile.items():
            firefox_profile.set_preference(key, value)

        firefox_options.profile = firefox_profile

        # Explicitly set the binary location
        firefox_options.binary_location = (
            r"C:\Program Files\Mozilla Firefox\firefox.exe"
        )
        firefox_options.add_argument("--headless")

        driver = webdriver.Firefox(
            service=FirefoxService(executable_path=GeckoDriverManager().install()),
            options=firefox_options,
        )

        try:
            driver.get("https://anabin.kmk.org/no_cache/filter/institutionen.html")

            wait = WebDriverWait(driver, 10)
            driver.find_element(By.XPATH, '//*[@id="searchTabs"]/ul/li[2]').click()
            driver.find_element(By.XPATH, '//*[@id="land-auswaehlen-"]').click()
            driver.find_element(By.XPATH, '//*[@id="check-land-216"]').click()
            driver.find_element(By.XPATH, '//*[@id="close"]').click()
            select_element = driver.find_element(
                By.XPATH, '//*[@id="institutionstabelle_length"]/label/select'
            )
            select = Select(select_element)
            select.select_by_value("100")
            search_field = driver.find_element(
                By.XPATH, '//*[@id="searchTabs-2"]/div[4]/div[1]/input[1]'
            )
            search_field.send_keys(institution_name)
            sleep(3)
            highlighted_element = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "highlight"))
            )

            driver.save_screenshot("screenshot.png")

            parent_row = highlighted_element.find_element(By.XPATH, "./ancestor::tr")

            parent_row.find_element(By.XPATH, "./td[1]/img").click()

            sleep(5)

            buttons = driver.find_element(By.XPATH, '//*[@id="service-buttons"]')
            sleep(5)
            driver.save_screenshot("screenshot3.png")

            # Example:
            print("Before printing...")
            buttons.find_element(By.ID, "print").click()
            print("After printing...")
            sleep(5)

        except NoSuchElementException:
            logging.warning(f"print not found")
        except StaleElementReferenceException:
            logging.warning(f"Stale element reference")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            print(f"Error: {str(e)}")
        finally:
            driver.quit()


def main():
    data = Download()
    institution_name = "Ecole de l'Aviation de Borj El Amri"
    data.fetch_data(institution_name)


if __name__ == "__main__":
    main()
