__version__ = "0.1.0"
import os
import time
from datetime import datetime
import logging

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(
    filename="check_appointment.log", format=FORMAT, level=logging.DEBUG
)

# Create a custom logger
logger = logging.getLogger("LandesamtEinwanderung")
logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.WARN)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARN)


from page_objects.landesamt_einwanderung import LandesamtEinwanderung
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


def main():
    logger.debug("Starting Selenium")
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-infobars")

    driver = webdriver.Chrome(options=options)
    logger.debug("Start page interations")
    page = (
        LandesamtEinwanderung(driver)
        .open()
        .bookAnAppointment()
        .acceptTerms()
        .clickNext()
        .selectCountry("323")
        .selectPeople("1")
        .selectFamily("2")
        .selectAppointmentType("SERVICEWAHL_DE3323-0-2")
        .selectVisaCategory("SERVICEWAHL_DE_323-0-2-1")
        .selectVisaType("SERVICEWAHL_DE323-0-2-1-329328")
        .clickNext()
    )

    session_time = datetime.strptime(page.getSessionTime(), "%M:%S")

    TEST_EXECUTION_TIME = 1
    while session_time.minute > TEST_EXECUTION_TIME:
        logger.debug(f"The session has {session_time.minute}min left")
        messages = page.get_page_messages()

        if len(messages) == 0:
            os.system(
                'osascript -e \'display alert "Check the selenium window" message "There might be an appointment available!"\''
            )
            logger.debug("No messages were returned, sleeping for 5 minutes")
            time.sleep(300)
        else:
            logger.debug("No appointments, sleeping for 10 seconds")
            time.sleep(10)
        session_time = datetime.strptime(page.getSessionTime(), "%M:%S")
        page.clickNext()
    logger.debug("Seessiong time finised")
    driver.quit()


if __name__ == "__main__":
    main()
