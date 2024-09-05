from sputnikqa.selenium_booster.enums import WaitCondition
from sputnikqa.utils.setup_logging import logger
from sputnikqa.selenium_booster.web_elements import Element
from sputnikqa.exceptions import BrokenException


class CheckBox(Element):
    def _click(self):
        self.find_element(wait_condition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED)

        super().click()
        return self

    def is_checked(self) -> bool:
        self.find_element()
        element_class = self.get_attribute_value('class')
        if 'uncheck' not in element_class:
            return True

    def check(self, check: bool = False):
        self.find_element(wait_condition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED)

        logger.debug(f'{self.full_name} check')
        if self.is_checked():
            raise BrokenException(f'{self.page_name}.{self.name} already checked')

        self._click()

        if check:
            if not self.is_checked():
                raise BrokenException(f'{self.page_name}.{self.name} is not checked')
        logger.info(f'{self.full_name} checked')

    def uncheck(self, check: bool = False):
        self.find_element(wait_condition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED)

        logger.debug(f'{self.full_name} uncheck')
        if not self.is_checked():
            raise BrokenException(f'{self.page_name}.{self.name} already unchecked')

        self._click()

        if check:
            if self.is_checked():
                raise BrokenException(f'{self.page_name}.{self.name} is not unchecked')
        logger.info(f'{self.full_name} unchecked')
