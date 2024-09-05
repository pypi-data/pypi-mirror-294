from abc import ABCMeta, abstractmethod

from sputnikqa.selenium_booster.web_elements.base.base_element import BaseElement, BaseWebElement


class BaseComplexElem(BaseElement, metaclass=ABCMeta):
    @abstractmethod
    def init_elements(self):
        # self.el_1 = BaseElement()
        pass

    def __init__(self, container: BaseWebElement):
        super().__init__()
        self.container = container
        self.init_elements()

    def find_element(self):
        self.container.find_element()

    def set_name(self, name: str, page_name: str):
        super().set_name(name, page_name)
        for attr_name, attr_value in self.__dict__.items():
            if isinstance(attr_value, BaseElement):
                attr_value.set_name(attr_name, f'{self.page_name}.{self.name}')

    def set_browser(self, driver):
        super().set_browser(driver)
        for attr_name, attr_value in self.__dict__.items():
            if isinstance(attr_value, BaseElement):
                attr_value.set_browser(driver)
