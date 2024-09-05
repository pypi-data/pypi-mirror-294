from selenium.webdriver.support.select import Select

from sputnikqa.selenium_booster.web_elements import Element
from sputnikqa.selenium_booster.enums import WaitCondition


class Selector(Element):
    def select(self, text: str):
        self.find_element(wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE)
        select_elem = Select(self.web_element)
        select_elem.select_by_visible_text(text)
