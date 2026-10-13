# -*- coding: utf-8 -*-
"""Тесты заказа самоката и переходов по логотипам."""
import allure
import pytest

from data import OrderData, Urls
from pages.main_page import MainPage
from pages.order_page import OrderPage


@allure.suite('Заказ самоката')
@allure.title('Позитивный сценарий заказа самоката')
class TestScooterOrder:
    """Позитивный флоу заказа: две точки входа и два набора данных.

    Сценарий общий, поэтому каждый набор данных тестируем из своей точки
    входа: верхняя кнопка «Заказать» + первый набор, нижняя кнопка +
    второй набор. Так обе точки входа покрыты без дублирования.
    """

    @pytest.mark.parametrize(
        'entry_point, order_data',
        [
            pytest.param('top', OrderData.FIRST_ORDER, id='Точка входа: кнопка в шапке'),
            pytest.param('bottom', OrderData.SECOND_ORDER, id='Точка входа: кнопка внизу страницы'),
        ],
    )
    def test_create_order_from_entry_point(self, driver, entry_point, order_data):
        main_page = MainPage(driver)
        main_page.open()
        main_page.accept_cookies()

        # Входим в сценарий через нужную точку входа
        main_page.click_order_button(entry_point)

        # Заполняем форму заказа и подтверждаем
        order_page = OrderPage(driver)
        order_page.create_order(order_data)

        # Появилось окно об успешном создании заказа
        assert order_page.is_success_modal_appeared()


@allure.suite('Логотипы')
class TestScooterLogos:
    """Проверка переходов по логотипам «Самоката» и Яндекса."""

    @allure.title('Клик по логотипу «Самоката» возвращает на главную страницу')
    def test_click_samokat_logo_goes_to_main_page(self, driver):
        main_page = MainPage(driver)
        main_page.open()
        main_page.accept_cookies()

        # Уходим со главной на страницу заказа
        main_page.click_order_button('top')
        order_page = OrderPage(driver)
        order_page.wait_for_visibility(order_page.NAME_INPUT)
        assert 'order' in driver.current_url

        # Клик по логотипу «Самоката» возвращает на главную страницу
        main_page.click_samokat_logo()
        assert driver.current_url == Urls.MAIN_PAGE

    @allure.title('Клик по логотипу Яндекса открывает главную страницу Дзена в новом окне')
    def test_click_yandex_logo_opens_dzen_in_new_window(self, driver):
        main_page = MainPage(driver)
        main_page.open()
        main_page.accept_cookies()

        main_page.click_yandex_logo()

        # Открывается новое окно, куда через редирект попадаем на Дзен
        main_page.switch_to_new_window()
        main_page.wait_for_url_contains(Urls.DZEN_HOST)
        assert Urls.DZEN_HOST in driver.current_url
