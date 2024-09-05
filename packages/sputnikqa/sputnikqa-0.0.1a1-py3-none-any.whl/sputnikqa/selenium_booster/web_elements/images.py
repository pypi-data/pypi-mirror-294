from sputnikqa.selenium_booster.enums import WaitCondition
from sputnikqa.selenium_booster.web_elements import Element


class Image(Element):
    def find_element(self, wait_sec: int = 10,
                     wait_condition: WaitCondition = WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED,
                     should_be_found: bool = True, use_previously_found_web_element: bool = True):

        super().find_element(wait_sec, wait_condition, should_be_found, use_previously_found_web_element)

    def get_size(self) -> dict:
        self.find_element()
        return self.web_element.size
