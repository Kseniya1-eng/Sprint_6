# -*- coding: utf-8 -*-
"""Базовый класс Page Object с общими методами работы с браузером."""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Общие методы для всех страниц."""

    def __init__(self, driver):
        self.driver = driver

    def wait_for_visibility(self, locator, timeout=10):
        """Дождаться видимости элемента и вернуть его."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=10):
        """Дождаться кликабельности элемента и вернуть его."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_text(self, locator, text, timeout=15):
        """Дождаться появления текста в элементе."""
        return WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )

    def click(self, locator, timeout=10):
        """Кликнуть по элементу (с ожиданием кликабельности)."""
        self.wait_for_clickable(locator, timeout).click()

    def input_text(self, locator, text, timeout=10):
        """Ввести текст в поле (с предварительной очисткой)."""
        element = self.wait_for_visibility(locator, timeout)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator, timeout=10):
        """Получить текст видимого элемента."""
        return self.wait_for_visibility(locator, timeout).text

    def scroll_to_element(self, locator, timeout=10):
        """Проскроллить страницу до элемента и вернуть его."""
        element = self.wait_for_visibility(locator, timeout)
        self.driver.execute_script('arguments[0].scrollIntoView();', element)
        return element

    def switch_to_new_window(self, timeout=10):
        """Переключиться на последнее открытое окно/вкладку."""
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.window_handles) > 1
        )
        new_window = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_window)
        return self.driver.current_url

    def wait_for_url_contains(self, text, timeout=20):
        """Дождаться, пока в адресе текущего окна появится текст.

        Нужно для редиректов, например с логотипа Яндекса на Дзен.
        """
        WebDriverWait(self.driver, timeout).until(
            lambda d: text in d.current_url
        )
