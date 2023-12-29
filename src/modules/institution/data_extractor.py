from data_extractor import DataExtractor
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
)


class UniversityDataExtractor(DataExtractor):
    def extract_data(self, row):
        columns = row.find_elements(By.TAG_NAME, "td")
        university_info = [col.text if col.text else "-" for col in columns]
        return (
            university_info[1],
            university_info[2],
            university_info[3],
            university_info[4],
            university_info[5],
            university_info[6],
        )

    def extract_cell_table(self, row):
        return self.extract_cell_table(row)

    def extract_diploma_data(self, driver) -> list:
        try:
            table = driver.find_element(
                By.XPATH, '//*[@id="accordion"]/div[3]/div/table'
            )
            rows = table.find_elements(By.TAG_NAME, "tr")

            formatted_data = []

            for row in rows:
                data = self.extract_cell_second_table(row)
                formatted_data.append(data)
            return formatted_data
        except NoSuchElementException as e:
            print(f"Error extracting diploma data: {str(e)}")
            return None
