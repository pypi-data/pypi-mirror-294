from sputnikqa.selenium_booster.enums import WaitCondition
from sputnikqa.selenium_booster.web_elements import Element
from sputnikqa.exceptions import BrokenException


class RadioButton(Element):
    def click(self):
        self.find_element(wait_condition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED)

        self.browser.get_driver().execute_script(f"arguments[0].click();", self.web_element)
        # super().click()
        return self

    def is_selected(self) -> bool:
        self.find_element()

        return self.web_element.is_selected()

    def select(self, check: bool = False):
        self.find_element(wait_condition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED)

        if self.is_selected():
            raise BrokenException(f'{self.page_name}.{self.name} already selected')

        self.click()

        if check:
            if not self.is_selected():
                raise BrokenException(f'{self.page_name}.{self.name} is not selected')
