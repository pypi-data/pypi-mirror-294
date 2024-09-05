from sputnikqa.selenium_booster.enums import WaitCondition
from sputnikqa.exceptions import BrokenException
from sputnikqa.selenium_booster.web_elements import Element
from time import sleep


# class AbstractTextField(metaclass=ABCMeta):
#     @abstractmethod
#     def insert_text(self, test: str) -> "AbstractTextField":
#         pass
#
#     @abstractmethod
#     def get_text(self) -> str:
#         pass
#
#     @abstractmethod
#     def clear(self) -> "AbstractTextField":
#         pass

class LabelField(Element):
    def get_text(self) -> str:
        self.find_element(wait_condition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED)

        return super().get_text()


class InputField(Element):
    def send_keys(self, keys: str):
        self.find_element(wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE)

        super().send_keys(keys)

    def send_keys_slow(self, keys: str):
        self.find_element(wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE)

        for key in keys:
            super().send_keys(key)
            sleep(1)

    def get_text(self) -> str:
        self.find_element(wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE)

        return self.get_attribute_value('value')

    def clear_field(self):
        self.find_element(wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE)

        self.clear()
        return self

    def input_text(self, text: str, send_keys_method=None, clear: bool = False, check: bool = False):
        self.find_element(wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE)

        if clear:
            self.clear_field()

        if not send_keys_method:
            self.send_keys(text)
        else:
            send_keys_method(text)

        if check:
            value = self.get_text()
            if value != text:
                raise BrokenException(f'The text does not match expected\n'
                                      f'expected:"{text}"\n'
                                      f'actual:"{value}"')
        return self


class TextArea(Element):
    pass


class UploadFileField(Element):
    def upload_file(self, file_path):
        self.find_element().send_keys(file_path)
