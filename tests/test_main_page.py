# -*- coding: utf-8 -*-
"""Тесты выпадающего списка в разделе «Вопросы о важном» главной страницы."""
import allure
import pytest

from data import FaqData
from pages.main_page import MainPage


@allure.suite('Главная страница')
@allure.title('Выпадающий список в разделе «Вопросы о важном»')
class TestFaqOnMainPage:
    """Проверка, что при клике на вопрос открывается соответствующий ответ."""

    @pytest.mark.parametrize(
        'question_data',
        FaqData.FAQ,
        ids=[item[1] for item in FaqData.FAQ],
    )
    def test_click_question_opens_matching_answer(self, driver, question_data):
        # Распаковываем набор данных: индекс, текст вопроса, ожидаемый ответ
        index, question, expected_answer = question_data

        main_page = MainPage(driver)
        main_page.open()
        main_page.accept_cookies()

        # Прокручиваем к разделу «Вопросы о важном» и открываем вопрос
        main_page.scroll_to_faq()
        main_page.click_question(index)

        # Открылся соответствующий текст ответа
        actual_answer = main_page.get_answer_text(index)
        assert actual_answer == expected_answer, (
            f'Ответ на вопрос {question!r} не совпадает с ожидаемым'
        )
