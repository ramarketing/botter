import pdb
import time


from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

from .logger import BaseLogger


class BaseRobot:

    def __init__(
        self, selenium_url, capabilities, base_dir, logger=None, debug=False,
        max_retries=5, *args, **kwargs
    ):
        self.logger = logger or BaseLogger(base_dir=base_dir, debug=self.debug)

        assert isinstance(logger, BaseLogger), (
            'Logger must be a BaseLogger instance.'
        )

        self.selenium_url = selenium_url
        self.capabilities = capabilities
        self.max_retries = max_retries
        self.debug = debug

    def get_driver(self, size=None):
        if hasattr(self, 'driver') and self.driver:
            return self.driver

        driver = webdriver.Remote(
            command_executor=self.selenium_url,
            desired_capabilities=self.capabilities
        )

        if size:
            try:
                width, height = size
                driver.set_window_size(int(width), int(height))
            except (TypeError, ValueError):
                pass

        while len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            self.wait(2)

        return driver

    def quit_driver(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.logger(data="Closing at {}.".format(self.driver.current_url))
            self.driver.quit()
        except AttributeError:
            pass

    def perform_action(func):
        def wrapper(self, by, selector, *args, **kwargs):
            retry = 0
            success = False

            try:
                timeout = int(kwargs.get('timeout', 0))
            except ValueError:
                timeout = 0

            return_method = func.__name__.startswith('get_')
            raise_exception = kwargs.get('raise_exception', True)

            if timeout:
                self.wait(timeout)

            while not success:
                retry += 1

                if retry > self.max_retries:
                    if raise_exception:
                        self._start_debug()
                        raise TimeoutException
                    else:
                        return success

                try:
                    if not isinstance(selector, (list, tuple)):
                        selector = [selector]

                    for s in selector:
                        try:
                            self.logger(data={
                                'action': func.__name__,
                                'selector': s,
                                'args': args,
                                'retry': retry,
                            })
                            response = func(self, by, s, *args, **kwargs)
                            success = True
                            break
                        except Exception:
                            pass
                    if not success:
                        raise TimeoutException
                except (TimeoutException, WebDriverException):
                    self.wait(1)

            return response if return_method else success

        return wrapper

    @perform_action
    def click_element(
        self, by, selector, source=None, move=False, *args, **kwargs
    ):
        final_source = source or self.driver
        element = final_source.find_element(by, selector)

        if move:
            ActionChains(self.driver) \
                .move_to_element(source or element) \
                .perform()

        disabled = element.get_attribute('aria-disabled')
        if disabled == 'true':
            self.wait(5)
            raise WebDriverException
        element.click()

    @perform_action
    def clear_input(self, by, selector, source=None, *args, **kwargs):
        source = source or self.driver
        element = source.find_element(by, selector)
        element.clear()

    @perform_action
    def fill_input(self, by, selector, content, source=None, *args, **kwargs):
        source = source or self.driver
        element = source.find_element(by, selector)
        element.send_keys(content)

    @perform_action
    def get_text(self, by, selector, source=None, *args, **kwargs):
        source = source or self.driver
        element = source.find_element(by, selector)
        return element.text

    @perform_action
    def get_element(
        self, by, selector, source=None, move=False, *args, **kwargs
    ):
        source = source or self.driver
        element = source.find_element(by, selector)

        if move:
            ActionChains(self.driver) \
                .move_to_element(source or element) \
                .perform()

        return element

    @perform_action
    def get_elements(self, by, selector, source=None, *args, **kwargs):
        source = source or self.driver
        elements = source.find_elements(by, selector)
        if len(elements) == 0:
            raise WebDriverException
        return elements

    def handle(self):
        raise NotImplementedError("`handle` nor implemented in the Base.")

    def wait(self, seconds):
        for second in range(seconds):
            if self.debug:
                print('Wait: {:d}/{:d}'.format(second + 1, seconds))
            time.sleep(1)

    def _start_debug(self, *args, **kwargs):
        if 'message' in kwargs:
            print(kwargs['message'])
        if self.debug:
            pdb.set_trace()
