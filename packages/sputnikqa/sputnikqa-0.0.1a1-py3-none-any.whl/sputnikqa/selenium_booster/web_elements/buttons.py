from selenium.webdriver import ActionChains

from sputnikqa.selenium_booster.enums import WaitCondition
from sputnikqa.utils.setup_logging import logger
from sputnikqa.selenium_booster.web_elements import Element


class Button(Element):
    def click(self):
        self.find_element(wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE)

        logger.debug(f'{self.full_name} click')
        super().click()
        logger.info(f'{self.full_name} clicked')
        return self

    def double_click(self):
        self.find_element(wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE)

        logger.debug(f'{self.full_name} double_click')
        action_chains = ActionChains(self.browser.get_driver())
        action_chains.double_click(self.web_element).perform()
        logger.info(f'{self.full_name} double_clicked')

    def right_click(self):
        self.find_element(wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE)

        logger.debug(f'{self.full_name} right_click')
        action_chains = ActionChains(self.browser.get_driver())
        action_chains.context_click(self.web_element).perform()
        logger.info(f'{self.full_name} right_clicked')
        return self
