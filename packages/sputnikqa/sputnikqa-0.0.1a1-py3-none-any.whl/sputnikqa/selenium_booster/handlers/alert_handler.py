from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sputnikqa.selenium_booster.browsers.base_browser import BaseBrowser


class AlertHandler:
    def __init__(self, browser: BaseBrowser):
        self.browser = browser

    def wait_for_alert(self, timeout: int = 10) -> Alert:
        """
        Ожидать появления алерта и переключиться на него.
        """
        #todo: selenium.common.exceptions.TimeoutException
        WebDriverWait(self.browser.get_driver(), timeout).until(EC.alert_is_present())
        return self.browser.get_driver().switch_to.alert

    def accept_alert(self):
        """
        Ожидать и принять алерт.
        """
        self.wait_for_alert().accept()

    def dismiss_alert(self):
        """
        Ожидать и отклонить алерт.
        """
        self.wait_for_alert().dismiss()

    def get_alert_text(self) -> str:
        """
        Ожидать и получить текст алерта.
        """
        alert = self.wait_for_alert()
        return alert.text

    def send_keys_to_alert(self, text: str):
        """
        Ожидать и отправить текст в алерт (для prompt).
        """
        self.wait_for_alert().send_keys(text)
