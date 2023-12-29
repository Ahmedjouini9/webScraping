from selenium.webdriver.common.by import By


class Items:
    def first_table(self):
        return By.XPATH, '//*[@id="pageUID-35"]/div[7]/div[2]/table/tbody'

    def second_table(self):
        return By.XPATH, '//*[@id="accordion"]/div[1]/table[1]/tbody'

    def third_table(self):
        return By.XPATH, '//*[@id="accordion"]/div[1]/table[2]/tbody'

    def fourth_table(self):
        return By.XPATH, '//*[@id="accordion"]/div[1]/table[3]/tbody'

    def fifth_table(self):
        return By.XPATH, '//*[@id="accordion"]/div[1]/table[4]/tbody'

    def get_first_table_titles(self):
        return ["Land:", "Bildungsinstitution:", "Übergeordnete Institution"]

    def get_second_table_titles(self):
        return [
            "Langname",
            "Abkürzung",
            "Name auf Deutsch",
            "Anschrift",
            "Telefon",
            "Fax",
            "E-Mail",
            "Homepage",
            "Kommentar",
        ]

    def get_third_table_titles(self):
        return ["Aliasname"]

    def get_fourth_table_titles(self):
        return ["Arabisch", "Englisch"]

    def get_fifth_table_titles(self):
        return ["Veralteter Name"]
