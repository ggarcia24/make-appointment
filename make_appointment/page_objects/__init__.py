from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class BasePage(object):
    def __init__(self, driver):
        self.driver: WebDriver = driver

    def wait_until(
        self,
        expected_condition,
        timeout=10,
        poll_frequency=0.5,
        ignored_exceptions=None,
    ):
        WebDriverWait(
            self.driver,
            timeout,
            poll_frequency,
            ignored_exceptions,
        ).until(expected_condition)

    def scroll_to_element(self, condition):
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element(*condition)).perform()
