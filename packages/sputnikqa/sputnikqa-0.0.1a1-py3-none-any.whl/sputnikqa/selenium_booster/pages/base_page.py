from abc import ABCMeta, abstractmethod
from contextlib import contextmanager

from sputnikqa.selenium_booster.browsers.base_browser import BaseBrowser
from sputnikqa.selenium_booster.web_elements import BaseElement, Iframe
from sputnikqa.selenium_booster.handlers.alert_handler import AlertHandler


class BasePage(metaclass=ABCMeta):
    @abstractmethod
    def init_elements(self):
        # self.el_1 = BaseElement()
        pass

    @abstractmethod
    def check_page_loaded(self):
        pass

    @contextmanager
    def frame_manager(self, frame_element: Iframe):
        # Внутри вызова __enter__
        el = frame_element.find_element().get_web_element()
        self.browser.get_driver().switch_to.frame(el)
        try:
            yield
        finally:
            # Внутри вызова __exit__
            self.browser.get_driver().switch_to.default_content()

    def __init__(self, browser: BaseBrowser):
        self.browser = browser
        self.init_elements()
        self.alert_handler = AlertHandler(self.browser)

        # for attr_name, attr_value in self.__class__.__dict__.items():
        for attr_name, attr_value in self.__dict__.items():
            if isinstance(attr_value, BaseElement):
                attr_value.set_browser(self.browser)

    def __setattr__(self, name, page_element_obj):
        if isinstance(page_element_obj, BaseElement):
            page_element_obj.set_name(name=name, page_name=self.__class__.__name__)
        super().__setattr__(name, page_element_obj)
