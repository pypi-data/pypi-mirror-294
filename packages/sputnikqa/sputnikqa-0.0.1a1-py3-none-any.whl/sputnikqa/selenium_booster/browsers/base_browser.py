from selenium import webdriver
from selenium.webdriver import Remote, Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions

from sputnikqa.selenium_booster.browsers.requests_manager import RequestsManager
from sputnikqa.selenium_booster.browsers.tab_manager import TabManager
from sputnikqa.selenium_booster.browsers.window_manager import WindowManager


class BaseBrowser:
    def __init__(self, browser_name="chrome"):
        self.browser_name = browser_name
        self.tab_manager = TabManager()
        self.window_manager = WindowManager()
        self.requests_manager = RequestsManager()
        self.driver = None

    def get_driver(self) -> Remote:
        if not self.driver:
            pass
        return self.driver

    def get_current_url(self) -> str:
        return self.get_driver().current_url

    def execute_js(self, script: str, *args):
        return self.get_driver().execute_script(script, *args)

    def get_session_id(self) -> str:
        return self.get_driver().session_id

    def open_browser(self):
        raise NotImplementedError("This method should be implemented by subclasses")

    def open_url(self, url: str):
        try:
            self.get_driver().get(url)
        except Exception as e:
            # selenium.common.exceptions.WebDriverException: Message: unknown error: net::ERR_SSL_PROTOCOL_ERROR
            raise Exception(f'Не открывается страница "{url}", подробнее: {e}') from None

    def close_browser(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None


class LocalBrowser(BaseBrowser):
    def open_browser(self):
        if self.browser_name == "chrome":
            options = ChromeOptions()
            options.page_load_strategy = 'none'
            prefs = {"download.default_directory": r"C:\Projects\PythonProjects\qagalaxy-alfa\z_test\test_data"}
            options.add_experimental_option("prefs", prefs)
            # enable logging
            options.add_argument('--enable-logging')
            options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

            driver: Chrome = webdriver.Chrome(options=options)
            driver.set_window_size(1920, 1080)
            driver.set_window_position(0, 0)
            # driver.maximize_window()
            self.driver = driver
        elif self.browser_name == "firefox":
            self.driver = webdriver.Firefox()
        else:
            raise ValueError(f"Unsupported browser: {self.browser_name}")
        self.tab_manager.driver = self.driver
        self.window_manager.driver = self.driver
        self.requests_manager.driver = self.driver


class RemoteBrowser(BaseBrowser):
    def open_browser(self):
        pass
    # if config.USE_REMOTE_SELENIUM:
    #     options = Options()
    #
    #     options.set_capability('browserName', 'chrome')
    #     # options.set_capability('browserVersion', '114.0')
    #     options.set_capability('selenoid:options', {
    #         "enableVNC": True,
    #         "enableVideo": False,
    #         "name": 'allure_parser'
    #     })
    #
    #     driver: Remote = webdriver.Remote(
    #         command_executor=config.SELENIUM_REMOTE_URL,
    #         options=options)
    #
    # else:
    #     # from selenium.webdriver.chrome.service import Service as ChromeService
    #     # driver = webdriver.Chrome(service=ChromeService(executable_path=r'C:\drivers\chromedriver.exe'))
    #     driver: Chrome = webdriver.Chrome()
