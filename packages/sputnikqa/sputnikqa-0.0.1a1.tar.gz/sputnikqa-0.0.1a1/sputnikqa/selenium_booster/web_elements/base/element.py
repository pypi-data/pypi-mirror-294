from selenium.common import NoSuchElementException
from selenium.common import StaleElementReferenceException, TimeoutException, InvalidSelectorException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from sputnikqa.selenium_booster.enums import WaitCondition
from sputnikqa.exceptions import BrokenException
from sputnikqa.utils.setup_logging import logger
from .base_element import BaseWebElement


class Element(BaseWebElement):
    def wait_presence_of_element(self, wait_sec: int, should_be_found: bool):
        """validate element in DOM"""
        if not self.parent:
            parent = self.browser.get_driver()
        else:
            parent = self.parent.get_web_element()

        try:
            self.web_element = WebDriverWait(parent, wait_sec).until(
                EC.presence_of_element_located((self.by, self.locator))
            )
        except TimeoutException:
            if should_be_found:
                raise BrokenException(
                    f'Element {self.page_name}.{self.name} not found in DOM for {wait_sec} sec') from None
        except InvalidSelectorException:
            raise BrokenException(
                f'Invalid locator {self.by}:"{self.locator}" on {self.page_name}.{self.name}') from None

    def wait_visibility_of_element(self, wait_sec: int, should_be_found: bool):
        """validate element in DOM and visible"""
        if not self.parent:
            parent = self.browser.get_driver()
        else:
            parent = self.parent.get_web_element()

        try:
            self.web_element = WebDriverWait(parent, wait_sec).until(
                EC.visibility_of_element_located((self.by, self.locator))
            )
        except TimeoutException:
            if should_be_found:
                raise BrokenException(
                    f'Element {self.page_name}.{self.name} not visible for {wait_sec} sec') from None
        except InvalidSelectorException:
            raise BrokenException(
                f'Invalid locator {self.by}:"{self.locator}" on {self.page_name}.{self.name}') from None

    def wait_element_to_be_clickable(self, wait_sec: int, should_be_found: bool):
        """validate element in DOM, visible and interactive"""
        if not self.parent:
            parent = self.browser.get_driver()
        else:
            parent = self.parent.get_web_element()

        try:
            self.web_element = WebDriverWait(parent, wait_sec).until(
                EC.element_to_be_clickable((self.by, self.locator))
            )
        except TimeoutException:
            if should_be_found:
                raise BrokenException(
                    f'Element {self.page_name}.{self.name} not clickable for {wait_sec} sec') from None
        except InvalidSelectorException:
            raise BrokenException(
                f'Invalid locator {self.by}:"{self.locator}" on {self.page_name}.{self.name}') from None

    def _find_element(self, wait_sec: int = 10,
                      wait_condition: WaitCondition = WaitCondition.PRESENCE_OF_ELEMENT_LOCATED,
                      should_be_found: bool = True):

        logger.debug(f'{self.full_name} find_element')

        if wait_sec != 0:
            if wait_condition == WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED:
                self.wait_visibility_of_element(wait_sec, should_be_found)
            elif wait_condition == WaitCondition.ELEMENT_TO_BE_CLICKABLE:
                self.wait_element_to_be_clickable(wait_sec, should_be_found)
            self.wait_presence_of_element(wait_sec, should_be_found)
        else:
            try:
                self.web_element = self.browser.get_driver().find_element(self.by, self.locator)
            except NoSuchElementException:
                if should_be_found:
                    raise BrokenException(f'Element {self.page_name}.{self.name} not found') from None

        logger.info(f'{self.full_name} found')
        return self

    def find_element(self, wait_sec: int = 10,
                     wait_condition: WaitCondition = WaitCondition.PRESENCE_OF_ELEMENT_LOCATED,
                     should_be_found: bool = True, use_previously_found_web_element: bool = True):

        if self.parent:
            self.parent.find_element()

        if not use_previously_found_web_element or not self.web_element:
            self._find_element(wait_sec, wait_condition, should_be_found)
        else:
            try:
                # if not fails, webelement still has the DOM object link
                _ = self.web_element.location
                logger.info(f'{self.full_name} was found before')
            except (StaleElementReferenceException, NoSuchElementException):
                self._find_element(wait_sec, wait_condition, should_be_found)

        if self.web_element._parent.session_id != self.browser.get_session_id():
            raise BrokenException('web_element.session_id != driver.session_id')

        return self
