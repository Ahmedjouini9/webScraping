from abc import ABC, abstractmethod


class FetchDataTemplate(ABC):
    def __init__(self):
        self.data_list = []

    @abstractmethod
    def fetch_data(self):
        raise NotImplementedError("Subclasses must implement the fetch_data method")

    @abstractmethod
    def fetch_cell_data(self, driver, row):
        raise NotImplementedError(
            "Subclasses must implement the fetch_cell_data method"
        )

    @abstractmethod
    def parse_to_excel(self, data_list):
        raise NotImplementedError("Subclasses must implement the parse_to_excel")

    @abstractmethod
    def filter_data(self, data_list, title_list):
        raise NotImplementedError("Subclasses must implement filter_data method")

    @abstractmethod
    def get_name():
        raise NotImplementedError("Must implement get_name methode")
