# -*- coding: utf-8 -*-
"""Фикстуры для автотестов."""
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


@pytest.fixture
def driver():
    """Открыть браузер Mozilla Firefox перед тестом и закрыть после."""
    options = Options()
    browser = webdriver.Firefox(options=options)
    browser.maximize_window()
    yield browser
    browser.quit()
