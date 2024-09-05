from typing import List

from selenium.webdriver.remote.webelement import WebElement

from sputnikqa.selenium_booster.browsers.base_browser import BaseBrowser
from sputnikqa.selenium_booster.enums import By
from sputnikqa.exceptions import BrokenException


class BaseElement:
    def __init__(self):
        self.name = None
        self.page_name = None
        self.browser: BaseBrowser | None = None

    # def __set_name__(self, owner, name: str):
    #     self.name = name
    #     self.page_name = owner.__name__

    @property
    def full_name(self) -> str:
        return f'{self.page_name}.({self.__class__.__name__}){self.name}'

    def set_name(self, name: str, page_name: str):
        self.name = name
        self.page_name = page_name

    def set_browser(self, browser: BaseBrowser):
        self.browser = browser

    """ -------------------------------------------- """




class BaseWebElement(BaseElement):
    def __init__(self, by: type(By), locator: str, parent: "BaseWebElement" = None):
        super().__init__()
        self.web_element: WebElement | None = None

        self.by = by
        self.locator = locator
        self.parent: BaseWebElement | None = parent

    def get_web_element(self) -> WebElement:
        if not self.web_element:
            raise BrokenException(f'{self.page_name}.{self.name} web_element is None')
        return self.web_element

    """ main functions """

    def find_element(self):
        if self.parent:
            self.web_element = self.parent.find_element().get_web_element().find_element(self.by, self.locator)
        else:
            self.web_element = self.browser.get_driver().find_element(self.by, self.locator)
        return self

    def find_elements(self) -> List[WebElement]:
        if self.parent:
            return self.parent.find_element().get_web_element().find_elements(self.by, self.locator)
        else:
            return self.browser.get_driver().find_elements(self.by, self.locator)

    def clear(self):
        self.get_web_element().clear()

    def click(self):
        self.get_web_element().click()

    def send_keys(self, keys):
        self.get_web_element().send_keys(keys)

    def is_displayed(self) -> bool:
        return self.get_web_element().is_displayed()

    def is_enabled(self) -> bool:
        return self.get_web_element().is_enabled()

    def get_text(self) -> str:
        return self.get_web_element().text

    def get_attribute_value(self, attrib_name: str) -> str:
        return self.get_web_element().get_attribute(attrib_name)
