from page_objects import BasePage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from typing_extensions import Self
from utils.loadable_page import LoadablePage, NotLoadedException


class LandesamtEinwanderung(BasePage, LoadablePage):
    def __init__(self, driver):
        super().__init__(driver)

    def _load(self):
        self.driver.get("https://otv.verwalt-berlin.de/ams/TerminBuchen")

    def _is_loaded(self):
        try:
            self.driver.find_element(By.LINK_TEXT, "Termin buchen")
        except:
            raise NotLoadedException("NOPE")

    def bookAnAppointment(self) -> Self:
        self.driver.find_element(By.LINK_TEXT, "Termin buchen").click()
        return self

    def acceptTerms(self) -> Self:
        condition = (By.ID, "xi-cb-1")
        self.wait_until(
            EC.all_of(
                EC.presence_of_element_located(condition),
                EC.element_to_be_clickable(condition),
            )
        )
        self.driver.find_element(*condition).click()
        return self

    def clickNext(self) -> Self:
        condition = (By.ID, "applicationForm:managedForm:proceed")
        self.wait_until(
            EC.all_of(
                EC.presence_of_element_located(condition),
                EC.element_to_be_clickable(condition),
            )
        )
        self.driver.find_element(*condition).click()
        return self

    def selectCoutry(self, country="") -> Self:
        condition = (By.ID, "xi-sel-400")
        self.wait_until(
            EC.all_of(
                EC.presence_of_element_located(condition),
                EC.visibility_of_element_located(condition),
            )
        )
        select = Select(self.driver.find_element(*condition))
        select.select_by_value(country)
        return self

    def selectPeople(self, amount="") -> Self:
        condition = (By.ID, "xi-sel-422")
        self.wait_until(
            EC.all_of(
                EC.presence_of_element_located(condition),
                EC.visibility_of_element_located(condition),
            )
        )
        select = Select(self.driver.find_element(*condition))
        select.select_by_value(amount)
        return self

    def selectFamily(self, answer="") -> Self:
        condition = (By.ID, "xi-sel-427")
        self.wait_until(
            EC.all_of(
                EC.presence_of_element_located(condition),
                EC.visibility_of_element_located(condition),
            )
        )
        select = Select(self.driver.find_element(*condition))
        select.select_by_value(answer)
        return self

    def selectAppointmentType(self, option="") -> Self:
        condition = (By.CSS_SELECTOR, f"label[for='{option}']")
        self.wait_until(
            EC.all_of(
                EC.presence_of_element_located(condition),
                EC.element_to_be_clickable(condition),
            )
        )
        self.scroll_to_element(condition)
        self.driver.find_element(*condition).click()
        return self

    def selectVisaCategory(self, option="") -> Self:
        condition = (By.CSS_SELECTOR, f"label[for='{option}']")
        self.wait_until(
            EC.all_of(
                EC.presence_of_element_located(condition),
                EC.element_to_be_clickable(condition),
            )
        )
        self.scroll_to_element(condition)
        self.driver.find_element(*condition).click()
        return self

    def selectVisaType(self, option="") -> Self:
        condition = (By.ID, option)
        self.wait_until(
            EC.all_of(
                EC.presence_of_element_located(condition),
                EC.element_to_be_clickable(condition),
            )
        )
        self.scroll_to_element(condition)
        self.driver.find_element(*condition).click()
        return self

    def get_page_messages(self):
        condition = (By.CSS_SELECTOR, "#messagesBox ul li.errorMessage")
        try:
            self.wait_until(
                EC.all_of(
                    EC.presence_of_element_located(condition),
                    EC.element_to_be_clickable(condition),
                )
            )
            return [element.text for element in self.driver.find_elements(*condition)]
        except TimeoutException:
            return []


#
