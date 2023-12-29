from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By


class DataExtractor(ABC):
    @abstractmethod
    def extract_data(self, row):
        raise NotImplementedError("Subclasses must implement the extract_data method")

    @abstractmethod
    def extract_cell_table(self, row):
        columns = row.find_elements(By.TAG_NAME, "td")
        returned_data = [col.text if col.text else "-" for col in columns]
        return returned_data
