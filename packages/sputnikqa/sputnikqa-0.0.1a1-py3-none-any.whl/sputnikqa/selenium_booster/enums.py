from enum import Enum
from selenium.webdriver.common.by import By as SeleniumCommonBy


class WaitCondition(Enum):
    PRESENCE_OF_ELEMENT_LOCATED = 'presence_of_element_located'
    VISIBILITY_OF_ELEMENT_LOCATED = 'visibility_of_element_located'
    ELEMENT_TO_BE_CLICKABLE = 'element_to_be_clickable'


class By(SeleniumCommonBy):
    pass
