import logging
from time import sleep
import pandas as pd
from MyProject.src.core.web_scraper import WebScraper
from selenium.webdriver.common.by import By
from MyProject.src.core.fetch_data_template import FetchDataTemplate
from data_extractor import UniversityDataExtractor
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from items import Items


class FetchUniversityData(FetchDataTemplate):
    def __init__(self, url):
        self.url = url
        self.information = []
        self.second_information = []

    def fetch_data(self):
        scraper = WebScraper(self.url)
        scraper.open_website()

        wait = WebDriverWait(scraper.driver, 10)

        scraper.click_element(By.XPATH, '//*[@id="searchTabs"]/ul/li[2]')
        scraper.click_element(By.XPATH, '//*[@id="land-auswaehlen-"]')
        scraper.click_element(By.XPATH, '//*[@id="check-land-216"]')
        scraper.click_element(By.XPATH, '//*[@id="close"]')
        select_element = scraper.find_elements(
            By.XPATH, '//*[@id="institutionstabelle_length"]/label/select'
        )[0]
        scraper.select_option_by_value(select_element, "100")
        sleep(2)
        while True:
            try:
                rows = scraper.find_elements(
                    By.XPATH, '//*[@id="institutionstabelle"]/tbody/tr'
                )
                for row in rows:
                    fetch_data = UniversityDataExtractor()
                    self.information.append(fetch_data.extract_data(row))
                    print(self.information)
                next_button = scraper.find_element(By.ID, "institutionstabelle_next")
                if "disabled" in next_button.get_attribute("class"):
                    break

                next_button.click()

                wait.until(EC.staleness_of(rows[0]))
            except Exception as e:
                print(f"Error in the loop: {str(e)}")
                break

        scraper.close_website()

    def fetch_cell_data(self, driver, row):
        returned_data1 = []
        returned_data2 = []
        returned_data3 = []
        returned_data4 = []
        try:
            sleep(2)
            cell = row.find_element(By.XPATH, "./td[1]")
            button = cell.find_elements(By.TAG_NAME, "img")

            if button:
                button[0].click()

                items = Items()
                sleep(2)
                print("After clicking button")

                returned_data1.extend(
                    self._fetch_table_data(
                        driver,
                        items.second_table(),
                        items.get_second_table_titles(),
                    )
                )
                returned_data2.extend(
                    self._fetch_table_data(
                        driver,
                        items.third_table(),
                        items.get_third_table_titles(),
                    )
                )
                returned_data3.extend(
                    self._fetch_table_data(
                        driver,
                        items.fourth_table(),
                        items.get_fourth_table_titles(),
                    )
                )
                returned_data4.extend(
                    self._fetch_table_data(
                        driver,
                        items.fifth_table(),
                        items.get_fifth_table_titles(),
                    )
                )
                print("After fetching table data")
                fetch_data = tuple()
                fetch_data += tuple(
                    item for sublist in returned_data1 for item in sublist
                )
                fetch_data += tuple(
                    item for sublist in returned_data2 for item in sublist
                )
                fetch_data += tuple(
                    item for sublist in returned_data3 for item in sublist
                )
                fetch_data += tuple(
                    item for sublist in returned_data4 for item in sublist
                )

                print(f"YEZEEEEEEEEEEEEEBYYYYY : {fetch_data}")

                # Additional debug statements
                print(f"returned_data1: {returned_data1}")
                print(f"returned_data2: {returned_data2}")
                print(f"returned_data3: {returned_data3}")
                print(f"returned_data4: {returned_data4}")

                try:
                    div = driver.find_element(By.XPATH, '//*[@id="service-buttons"]')
                    div.find_element(By.ID, "close").click()
                    print("im pressing this fuckking button")
                    sleep(2)
                except NoSuchElementException as e:
                    print(f"Error clicking close button: {str(e)}")

        except NoSuchElementException as e:
            print(f"Error finding button: {str(e)}")
        except Exception as e:
            print(f"Error clicking first cell: {str(e)}")

        return fetch_data

    def fetch_table_data(self, driver, table_function, title_function) -> list:
        returned_data = []
        result_data = []
        try:
            wait = WebDriverWait(driver, 3)
            table = wait.until(EC.visibility_of_element_located(table_function))
            rows = table.find_elements(By.TAG_NAME, "tr")
            print(f"Number of rows found: {len(rows)}")
            fetch_data = UniversityDataExtractor()

            if not rows:
                print("No rows found in the table.")
                return returned_data
            result_data = [fetch_data.extract_cell_table(row) for row in rows]
            returned_data.append(self.filter_data(result_data, title_function))

        except NoSuchElementException:
            logging.warning(f"Table not found for {table_function.__name__}")
            returned_data.extend(["-"] * len(title_function))
        except StaleElementReferenceException:
            logging.warning(
                f"Stale element reference while fetching data from table: {table_function.__name__}"
            )
            returned_data.extend(["-"] * len(title_function))
        except Exception as e:
            logging.error(f"Error fetching data from table: {str(e)}")
            print(f"Error fetching data from table: {str(e)}")
            returned_data.extend(["-"] * len(title_function))
        return returned_data

    def filter_data(self, data_list, title_names):
        data_dict = dict(data_list)
        result_data = [
            data_dict.get(title, "-") if isinstance(data_dict, dict) else "-"
            for title in title_names
        ]
        return result_data

    def parse_to_excel(self, data_list):
        df = pd.DataFrame(
            data_list,
            columns=[
                "InstitutionName",
                "InstitutionLocation",
                "InstitutionStatus",
                "InstitutionType",
                "InstitutionCountry",
                "InstitutionMother",
            ],
        )

        df.to_csv("Institution.csv", index=False)

    def parse_to_excel_two(self, data_list):
        df = pd.DataFrame(
            data_list,
            columns=[
                "Langname",
                "Abkurzung",
                "Anschrift",
                "Telefon",
                "Fax",
                "Email",
                "Homepage",
                "Kommentar",
                "Aliasname",
                "Aliasname2",
                "Englisch",
                "Arabisch",
                "status_Kommentar",
                "Institution",
            ],
        )
        df.to_excel("SecondInstitution.xlsx", index=False)

    def get_name(self, driver):
        pass


def main():
    url = "https://anabin.kmk.org/no_cache/filter/institutionen.html"
    data = FetchUniversityData(url)
    data.fetch_data()
    data.parse_to_excel(data.information)


if __name__ == "__main__":
    main()
