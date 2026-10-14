# -*- coding: utf-8 -*-
"""Базовый класс Page Object с общими методами работы с браузером."""
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Общие методы для всех страниц."""

    @allure.step('Инициализировать страницу')
    def __init__(self, driver):
        self.driver = driver

    @allure.step('Дождаться видимости элемента {locator}')
    def wait_for_visibility(self, locator, timeout=10):
        """Дождаться видимости элемента и вернуть его."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step('Дождаться кликабельности элемента {locator}')
    def wait_for_clickable(self, locator, timeout=10):
        """Дождаться кликабельности элемента и вернуть его."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    @allure.step('Дождаться появления текста {text} в элементе {locator}')
    def wait_for_text(self, locator, text, timeout=15):
        """Дождаться появления текста в элементе."""
        return WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )

    @allure.step('Кликнуть по элементу {locator}')
    def click(self, locator, timeout=10):
        """Кликнуть по элементу (с ожиданием кликабельности)."""
        self.wait_for_clickable(locator, timeout).click()

    @allure.step('Ввести текст в поле {locator}')
    def input_text(self, locator, text, timeout=10):
        """Ввести текст в поле (с предварительной очисткой)."""
        element = self.wait_for_visibility(locator, timeout)
        element.clear()
        element.send_keys(text)

    @allure.step('Получить текст элемента {locator}')
    def get_text(self, locator, timeout=10):
        """Получить текст видимого элемента."""
        return self.wait_for_visibility(locator, timeout).text

    @allure.step('Проскроллить страницу до элемента {locator}')
    def scroll_to_element(self, locator, timeout=10):
        """Проскроллить страницу до элемента и вернуть его."""
        element = self.wait_for_visibility(locator, timeout)
        self.driver.execute_script('arguments[0].scrollIntoView();', element)
        return element

    @allure.step('Кликнуть по элементу {locator} через JavaScript')
    def click_with_js(self, locator, timeout=10):
        """Проскроллить к элементу и кликнуть по нему через JavaScript.

        Нужно, когда элемент перекрыт другими слоями страницы и обычный
        клик может не сработать.
        """
        element = self.scroll_to_element(locator, timeout)
        self.driver.execute_script('arguments[0].click();', element)

    @allure.step('Открыть страницу {url}')
    def open_url(self, url):
        """Открыть указанный адрес."""
        self.driver.get(url)

    @allure.step('Получить адрес текущей страницы')
    def get_current_url(self):
        """Вернуть адрес текущей страницы."""
        return self.driver.current_url

    @allure.step('Переключиться на последнее открытое окно')
    def switch_to_new_window(self, timeout=10):
        """Переключиться на последнее открытое окно/вкладку."""
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.window_handles) > 1
        )
        new_window = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_window)
        return self.get_current_url()

    @allure.step('Дождаться появления текста {text} в адресной строке')
    def wait_for_url_contains(self, text, timeout=20):
        """Дождаться, пока в адресе текущего окна появится текст.

        Нужно для редиректов, например с логотипа Яндекса на Дзен.
        """
        WebDriverWait(self.driver, timeout).until(
            lambda d: text in d.current_url
        )
