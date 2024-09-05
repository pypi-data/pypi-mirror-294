from typing import List


class WindowManager:
    def __init__(self):
        self.driver = None

    def open_new_window(self, url: str | None = None):
        self.driver.execute_script("window.open('', '_blank');")
        self.switch_to_window(-1)
        if url:
            self.driver.get(url)

    def switch_to_window(self, index: int):
        try:
            self.driver.switch_to.window(self.driver.window_handles[index])
        except IndexError:
            raise ValueError(
                f'Tabs amount: {len(self.driver.window_handles)}, your index {index}')  # todo: переписать ошибку

    def get_windows_list(self) -> List[str]:
        return self.driver.window_handles

    def close_window(self, index: int | None = None):
        if index is not None:
            self.switch_to_window(index)
        self.driver.close()
        if len(self.driver.window_handles) > 0:
            self.switch_to_window(0)

    def get_current_window_id(self) -> str:
        return self.driver.current_window_handle
