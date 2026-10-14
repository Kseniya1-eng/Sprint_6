# -*- coding: utf-8 -*-
"""Page Object главной страницы сервиса «Яндекс.Самокат»."""
import allure
from selenium.webdriver.common.by import By

from data import Urls
from pages.base_page import BasePage


class MainPage(BasePage):
    """Главная страница: кнопки заказа, логотипы, раздел «Вопросы о важном»."""

    # Кнопки «Заказать»
    ORDER_BUTTON_TOP = (
        By.XPATH, "//div[contains(@class, 'Header_Nav')]//button[text()='Заказать']"
    )
    ORDER_BUTTON_BOTTOM = (
        By.XPATH, "//div[contains(@class, 'Home_FinishButton')]//button[text()='Заказать']"
    )

    # Логотипы в шапке
    YANDEX_LOGO = (By.XPATH, "//a[contains(@class, 'Header_LogoYandex')]")
    SAMOKAT_LOGO = (By.XPATH, "//a[contains(@class, 'Header_LogoScooter')]")

    # Баннер согласия на куки
    COOKIE_CONFIRM_BUTTON = (By.ID, 'rcc-confirm-button')

    # Раздел «Вопросы о важном»
    FAQ_SUBHEADER = (
        By.XPATH, "//div[contains(@class, 'Home_SubHeader') and contains(text(), 'Вопросы о важном')]"
    )

    @allure.step('Открыть главную страницу')
    def open(self):
        """Открыть главную страницу."""
        self.open_url(Urls.MAIN_PAGE)

    @allure.step('Закрыть баннер согласия на куки')
    def accept_cookies(self):
        """Закрыть баннер согласия на куки, если он появился."""
        try:
            self.wait_for_clickable(self.COOKIE_CONFIRM_BUTTON, timeout=5).click()
        except Exception:
            pass

    @allure.step('Кликнуть по кнопке «Заказать» ({position})')
    def click_order_button(self, position):
        """Кликнуть по кнопке «Заказать»: 'top' — в шапке, 'bottom' — внизу."""
        if position == 'bottom':
            self.scroll_to_element(self.ORDER_BUTTON_BOTTOM)
        self.click(self.ORDER_BUTTON_TOP if position == 'top' else self.ORDER_BUTTON_BOTTOM)

    @allure.step('Кликнуть по логотипу Яндекса')
    def click_yandex_logo(self):
        """Кликнуть по логотипу Яндекса (открывает новое окно)."""
        self.click(self.YANDEX_LOGO)

    @allure.step('Кликнуть по логотипу «Самоката»')
    def click_samokat_logo(self):
        """Кликнуть по логотипу «Самоката»."""
        self.click(self.SAMOKAT_LOGO)

    @allure.step('Проскроллить к разделу «Вопросы о важном»')
    def scroll_to_faq(self):
        """Проскроллить к разделу «Вопросы о важном»."""
        self.scroll_to_element(self.FAQ_SUBHEADER)

    @allure.step('Кликнуть по вопросу с индексом {index}')
    def click_question(self, index):
        """Кликнуть по вопросу с заданным индексом, чтобы открыть ответ.

        Используется клик через JavaScript: декоративная картинка самоката
        на главной странице иногда перекрывает вопрос и мешает обычному клику.
        """
        question = (By.ID, f'accordion__heading-{index}')
        self.click_with_js(question)

    @allure.step('Получить текст ответа на вопрос с индексом {index}')
    def get_answer_text(self, index):
        """Вернуть текст ответа на вопрос с заданным индексом."""
        answer = (By.XPATH, f"//div[@id='accordion__panel-{index}']//p")
        return self.get_text(answer)
