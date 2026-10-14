# -*- coding: utf-8 -*-
"""Page Object страницы оформления заказа «Яндекс.Самокат»."""
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class OrderPage(BasePage):
    """Страница заказа: форма из двух шагов и модальные окна."""

    # --- Шаг 1: «Для кого самокат» ---
    NAME_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Имя')]")
    SURNAME_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Фамилия')]")
    ADDRESS_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Адрес')]")
    METRO_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Станция метро')]")
    PHONE_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Телефон')]")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")

    # --- Шаг 2: «Про аренду» ---
    DATE_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Когда привезти самокат')]")
    RENTAL_PERIOD_DROPDOWN = (By.CLASS_NAME, 'Dropdown-control')
    COLOR_INPUT_CHECKBOX = (By.XPATH, "//label[@for='{color}']")
    COMMENT_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Комментарий')]")
    SUBMIT_ORDER_BUTTON = (
        By.XPATH, "//button[contains(@class, 'Button_Middle') and text()='Заказать']"
    )

    # --- Модальные окна ---
    CONFIRM_ORDER_BUTTON = (
        By.XPATH, "//div[contains(@class, 'Order_Modal')]//button[text()='Да']"
    )
    ORDER_MODAL_HEADER = (By.XPATH, "//div[contains(@class, 'Order_ModalHeader')]")
    SUCCESS_MESSAGE = 'Заказ оформлен'

    @allure.step('Получить локатор станции метро {station}')
    def metro_station_option(self, station):
        """Локатор станции метро в выпадающем списке."""
        return (
            By.XPATH,
            f"//button[contains(@class, 'select-search__option')]"
            f"[.//div[contains(@class, 'Order_Text') and text()='{station}']]"
        )

    @allure.step('Получить локатор срока аренды {period}')
    def rental_period_option(self, period):
        """Локатор срока аренды в выпадающем списке."""
        return (
            By.XPATH,
            f"//div[contains(@class, 'Dropdown-option') and text()='{period}']"
        )

    @allure.step('Выбрать станцию метро {station}')
    def select_metro_station(self, station):
        """Выбрать станцию метро из выпадающего списка."""
        self.click(self.METRO_INPUT)
        self.click(self.metro_station_option(station))

    @allure.step('Заполнить личные данные клиента')
    def fill_personal_data(self, data):
        """Заполнить первый шаг формы: данные о клиенте."""
        self.input_text(self.NAME_INPUT, data['name'])
        self.input_text(self.SURNAME_INPUT, data['surname'])
        self.input_text(self.ADDRESS_INPUT, data['address'])
        self.select_metro_station(data['metro_station'])
        self.input_text(self.PHONE_INPUT, data['phone'])
        self.wait_for_clickable(self.NEXT_BUTTON).click()

    @allure.step('Заполнить данные об аренде')
    def fill_rental_data(self, data):
        """Заполнить второй шаг формы: данные об аренде."""
        self.wait_for_visibility(self.DATE_INPUT)

        date_field = self.wait_for_visibility(self.DATE_INPUT)
        date_field.send_keys(data['date'] + Keys.ENTER)

        self.click(self.RENTAL_PERIOD_DROPDOWN)
        self.click(self.rental_period_option(data['rental_period']))

        color_checkbox = (By.XPATH, self.COLOR_INPUT_CHECKBOX[1].format(color=data['color']))
        self.click(color_checkbox)

        self.input_text(self.COMMENT_INPUT, data['comment'])

    @allure.step('Подтвердить заказ')
    def submit_order(self):
        """Подтвердить заказ: нажать «Заказать» и «Да» в модальном окне."""
        self.wait_for_clickable(self.SUBMIT_ORDER_BUTTON).click()
        self.wait_for_clickable(self.CONFIRM_ORDER_BUTTON).click()

    @allure.step('Оформить заказ')
    def create_order(self, data):
        """Полный позитивный сценарий оформления заказа."""
        self.fill_personal_data(data)
        self.fill_rental_data(data)
        self.submit_order()

    @allure.step('Проверить появление окна об успешном заказе')
    def is_success_modal_appeared(self):
        """Проверить, что появилось окно об успешном создании заказа."""
        return self.wait_for_text(self.ORDER_MODAL_HEADER, self.SUCCESS_MESSAGE)
