import logging

from page_objects import BasePage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from typing_extensions import Self
from utils.loadable_page import LoadablePage, NotLoadedException

logger = logging.getLogger("LandesamtEinwanderung")


class LandesamtEinwanderung(BasePage, LoadablePage):

    page_loading_selector = (By.CSS_SELECTOR, "body > div.loading")
    form_loading_selector = (
        By.CSS_SELECTOR,
        "[id='applicationForm:managedForm'] > div.loading",
    )

    def __init__(self, driver):
        super().__init__(driver)

    def _load(self):
        self.driver.get("https://otv.verwalt-berlin.de/ams/TerminBuchen")

    def _is_loaded(self):
        try:
            self.driver.find_element(By.LINK_TEXT, "Termin buchen")
        except:
            raise NotLoadedException("NOPE")

    def wait_for_overlays(self) -> Self:
        logger.debug("Waiting for overlays to go away")
        self.wait_until(
            EC.all_of(
                EC.invisibility_of_element_located(self.page_loading_selector),
                EC.invisibility_of_element_located(self.form_loading_selector),
            ),
            timeout=45,
        )

    def getSessionTime(self) -> str:
        self.wait_for_overlays()
        logger.debug("Getting session time")
        condition = (By.ID, "progressBar")
        self.wait_until(EC.presence_of_element_located(condition))
        return self.driver.find_element(*condition).text

    def bookAnAppointment(self) -> Self:
        logger.debug("Clicking link")
        self.driver.find_element(By.LINK_TEXT, "Termin buchen").click()
        self.wait_for_overlays()
        return self

    def acceptTerms(self) -> Self:
        logger.debug("Clicking Accept Terms checkbox")
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
        self.wait_for_overlays()
        logger.debug("Click the Next button")
        condition = (By.ID, "applicationForm:managedForm:proceed")
        self.wait_until(
            EC.all_of(
                EC.presence_of_element_located(condition),
                EC.element_to_be_clickable(condition),
            )
        )
        self.scroll_to_element(condition)
        self.driver.find_element(*condition).click()
        self.wait_for_overlays()
        return self

    def selectCountry(self, country="") -> Self:
        self.wait_for_overlays()
        logger.debug("Select Country")
        condition = (By.ID, "xi-sel-400")
        self.wait_until(
            EC.all_of(
                EC.presence_of_element_located(condition),
                EC.visibility_of_element_located(condition),
                EC.element_to_be_clickable(condition),
            ),
            timeout=45,
        )
        select = Select(self.driver.find_element(*condition))
        select.select_by_value(country)
        return self

    def selectPeople(self, amount="") -> Self:
        logger.debug("Select amount of people")
        condition = (By.ID, "xi-sel-422")
        self.wait_until(
            EC.all_of(
                EC.presence_of_element_located(condition),
                EC.element_to_be_clickable(condition),
                EC.visibility_of_element_located(condition),
            )
        )
        select = Select(self.driver.find_element(*condition))
        select.select_by_value(amount)
        self.wait_for_overlays()
        return self

    def selectFamily(self, answer="") -> Self:
        logger.debug("Select family option")
        condition = (By.ID, "xi-sel-427")
        self.wait_until(
            EC.all_of(
                EC.presence_of_element_located(condition),
                EC.element_to_be_clickable(condition),
                EC.visibility_of_element_located(condition),
            )
        )
        select = Select(self.driver.find_element(*condition))
        select.select_by_value(answer)
        self.wait_for_overlays()
        return self

    def selectAppointmentType(self, option="") -> Self:
        self.wait_for_overlays()
        logger.debug("Select Appointment Type")
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
        self.wait_for_overlays()
        logger.debug("Select Visa Category")
        condition = (By.CSS_SELECTOR, f"label[for='{option}']")
        self.wait_until(
            EC.all_of(
                EC.presence_of_element_located(condition),
                EC.element_to_be_clickable(condition),
            )
        )
        self.scroll_to_element(condition)
        self.driver.find_element(*condition).click()
        self.wait_for_overlays()
        return self

    def selectVisaType(self, option="") -> Self:
        self.wait_for_overlays()
        logger.debug("Select Visa Type")
        condition = (By.ID, option)
        self.wait_until(
            EC.all_of(
                EC.presence_of_element_located(condition),
                EC.element_to_be_clickable(condition),
            )
        )
        self.scroll_to_element(condition)
        self.driver.find_element(*condition).click()
        self.wait_for_overlays()
        return self

    def get_page_messages(self):
        self.wait_for_overlays()
        logger.debug("Getting page messages")
        condition = (By.CSS_SELECTOR, "#messagesBox ul li.errorMessage")
        try:
            self.wait_until(
                EC.all_of(
                    EC.presence_of_element_located(condition),
                    EC.element_to_be_clickable(condition),
                )
            )
            return [element.text for element in self.driver.find_elements(*condition)]
        except Exception as e:
            logger.error("Error occurred: ", exc_info=e)
            return []


#
