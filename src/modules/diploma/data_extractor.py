from data_extractor import DataExtractor
from selenium.webdriver.common.by import By


class DiplomaDataExtractor(DataExtractor):
    def extract_data(self, row):
        columns = row.find_elements(By.TAG_NAME, "td")
        university_info = [col.text if col.text else "N/A" for col in columns]
        return (
            university_info[1],
            university_info[2],
            university_info[3],
            university_info[4],
            university_info[5],
            university_info[6],
            university_info[7],
        )

    def extract_cell_table(self, row):
        return self.extract_cell_table(row)
