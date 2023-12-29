import logging
import pandas as pd
from time import sleep
from MyProject.src.core.web_scraper import WebScraper
from selenium.webdriver.common.by import By
from MyProject.src.core.fetch_data_template import FetchDataTemplate
from data_extractor import DiplomaDataExtractor
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)


class FetchDiplomaData(FetchDataTemplate):
    def __init__(self, url):
        self.url = url
        self.information = []
        self.returned_data1 = []
        self.returned_data2 = []
        # self.returned_data3 = []
        self.name = []

    def fetch_data(self):
        scraper = WebScraper(self.url)
        scraper.open_website()

        wait = WebDriverWait(scraper.driver, 10)

        scraper.click_element(By.XPATH, '//*[@id="searchTabs"]/ul/li[2]/a')
        scraper.click_element(By.XPATH, '//*[@id="land-auswaehlen-abschluss"]')
        scraper.click_element(By.XPATH, '//*[@id="check-land-216"]')
        scraper.click_element(By.XPATH, '//*[@id="close"]')
        select_element = scraper.find_elements(
            By.XPATH, '//*[@id="abschlusstabelle_length"]/label/select'
        )[0]
        scraper.select_option_by_value(select_element, "100")
        sleep(2)
        while True:
            try:
                rows = scraper.find_elements(
                    By.XPATH, '//*[@id="abschlusstabelle"]/tbody/tr'
                )
                for row in rows:
                    diploma_extract_data = DiplomaDataExtractor()
                    self.information.append(diploma_extract_data.extract_data(row))
                next_button = scraper.find_element(By.ID, "abschlusstabelle_next")
                if "disabled" in next_button.get_attribute("class"):
                    break

                next_button.click()

                wait.until(EC.staleness_of(rows[0]))
            except Exception as e:
                print(f"Error: {str(e)}")

        scraper.close_website()

    def fetch_cell_data(self, row, driver):
        try:
            sleep(2)
            cell = row.find_element(By.XPATH, "./td[1]")
            button = cell.find_elements(By.TAG_NAME, "img")

            if button:
                button[0].click()
                sleep(2)
                self.get_diploma_name(driver)
                print("After clicking button")
                self.fetch_table_data(driver)
                print(self.returned_data1)
                self.fetch_first_table(driver)
                print(self.returned_data2)
                self.fetch_second_table(driver)
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

    def parse_to_excel(self, data_list):
        df = pd.DataFrame(
            data_list,
            columns=[
                "DiplomaName",
                "DiplomaType",
                "minDuration",
                "maxDuration",
                "class",
                "field",
                "Country",
            ],
        )

        df.to_csv("diploma.csv", index=False)

    def filter_data(self, data_list, title_names):
        data_dict = dict(data_list)
        result_data = [
            data_dict.get(title, "-") if isinstance(data_dict, dict) else "-"
            for title in title_names
        ]
        return result_data

    def fetch_first_table_data(self, driver):
        try:
            wait = WebDriverWait(driver, 3)
            table = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="accordion"]/div[1]/table[1]/tbody')
                )
            )
            rows = table.find_elements(By.TAG_NAME, "tr")
            fetch_data = DiplomaDataExtractor()
            title = [
                "Abschluss (deutsche Übersetzung)",
                "Studienrichtung (deutsche Übersetzung)",
                "Kommentar",
            ]
            result_data = [fetch_data.extract_cell_table(row) for row in rows]
            row_data = self._filter_data(result_data, title)
            self.returned_data1.append(tuple(row_data) + tuple(self.name))

        except NoSuchElementException:
            logging.warning(f"Table not found for")
            self.returned_data1.append(tuple(["-"] * len(title)) + tuple(self.name))
        except StaleElementReferenceException:
            logging.warning(f"Stale element reference while fetching data from table")
            self.returned_data1.append(tuple(["-"] * len(title)) + tuple(self.name))
        except Exception as e:
            logging.error(f"Error fetching data from table: {str(e)}")
            print(f"Error fetching data from table: {str(e)}")
            self.returned_data1.append(tuple(["-"] * len(title)) + tuple(self.name))

    def fetch_second_table_data(self, driver):
        try:
            fetch_data = DiplomaDataExtractor()
            wait = WebDriverWait(driver, 3)
            table = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="accordion"]/div[1]/table[2]/tbody')
                )
            )
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                row_data = fetch_data.extract_cell_table(row)
            self.returned_data2.append(tuple(row_data) + tuple(self.name))
        except NoSuchElementException:
            logging.warning(f"Table not found for table")
            self.returned_data2.append(tuple(["-"] * 2) + tuple(self.name))
        except StaleElementReferenceException:
            logging.warning(f"Stale element reference while fetching data from table")
            self.returned_data2.append(tuple(["-"] * 2) + tuple(self.name))
        except Exception as e:
            logging.error(f"Error fetching data from table: {str(e)}")
            print(f"Error fetching data from table: {str(e)}")
            self.returned_data2.append(tuple(["-"] * 2) + tuple(self.name))

    def fetch_third_table(self, driver):
        try:
            fetch_data = DiplomaDataExtractor()
            wait = WebDriverWait(driver, 3)
            table = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="accordion"]/div[2]/div/table/tbody')
                )
            )
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                print(f"rows :{row}")
                self.returned_data3.append(tuple(fetch_data.extract_cell_table(row)))
                self.returned_data3.append(self.abschluss)
        except NoSuchElementException:
            logging.warning(f"Table not found for table")
            self.returned_data3.append(tuple(["-"] * 3))
        except StaleElementReferenceException:
            logging.warning(f"Stale element reference while fetching data from table: ")
            self.returned_data3.append(tuple(["-"] * 3))
        except Exception as e:
            logging.error(f"Error fetching data from table: {str(e)}")
            print(f"Error fetching data from table: {str(e)}")
            self.returned_data3.append(tuple(["-"] * 3))

    def get_name(self, driver):
        try:
            wait = WebDriverWait(driver, 3)
            self.name.clear()
            self.name.append(
                wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="pageUID-9"]/div[7]/div[2]/table/tbody/tr[2]/td',
                        ),
                    )
                ).text
            )
        except NoSuchElementException:
            logging.warning(f"Table not found for table")
            return [tuple(["-"])]
        except StaleElementReferenceException:
            logging.warning(f"Stale element reference while fetching data from table")
            return [tuple(["-"])]
        except Exception as e:
            logging.error(f"Error fetching data from table: {str(e)}")
            print(f"Error fetching data from table: {str(e)}")
            return [tuple(["-"])]


def main():
    url = "https://anabin.kmk.org/no_cache/filter/hochschulabschluesse.html"
    data = FetchDiplomaData(url)
    data.fetch_data()
    data.parse_to_excel(data.information)


if __name__ == "__main__":
    main()
