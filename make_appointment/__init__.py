__version__ = "0.1.0"
import os

from page_objects.landesamt_einwanderung import LandesamtEinwanderung
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


def main():
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    # options.add_argument("--start-maximized")
    # options.add_argument("--start-fullscreen")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-infobars")

    driver = webdriver.Chrome(options=options)
    page = (
        LandesamtEinwanderung(driver)
        .open()
        .bookAnAppointment()
        .acceptTerms()
        .clickNext()
        .selectCoutry("323")
        .selectPeople("1")
        .selectFamily("2")
        .selectAppointmentType("SERVICEWAHL_DE3323-0-2")
        .selectVisaCategory("SERVICEWAHL_DE_323-0-2-1")
        .selectVisaType("SERVICEWAHL_DE323-0-2-1-329328")
        .clickNext()
    )

    messages = page.get_page_messages()

    if len(messages) == 0:
        os.system(
            """
osascript -e 'display alert "Check the selenium window" message "There might be an appointment available!"
"""
        )
    else:
        print("No appointments in this run")
        driver.quit()


if __name__ == "__main__":
    main()
