from typing import List


class TabManager:
    def __init__(self):
        self.driver = None

    def open_new_tab(self, url: str | None = None):
        self.driver.execute_script("window.open('');")
        self.switch_to_tab(-1)
        if url:
            self.driver.get(url)

    def switch_to_tab(self, index: int):
        try:
            self.driver.switch_to.window(self.driver.window_handles[index])
        except IndexError:
            raise ValueError(f'Tabs amount: {len(self.driver.window_handles)}, your index {index}')  # todo: переписать ошибку

    def get_tabs_list(self) -> List[str]:
        return self.driver.window_handles

    def close_tab(self, index: int | None = None):
        if index is not None:
            self.switch_to_tab(index)
        self.driver.close()
        if len(self.driver.window_handles) > 0:
            self.switch_to_tab(0)

    def get_current_tab_id(self) -> str:
        return self.driver.current_window_handle
