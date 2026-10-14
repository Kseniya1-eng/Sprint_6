# -*- coding: utf-8 -*-
"""Автоматическая установка Allure CLI для генерации Allure-отчёта.

Запуск на любом компьютере (в том числе у проверяющего), если Allure ещё
не установлен:

    python install_allure.py

Скрипт скачивает и распаковывает Allure CLI рядом с проектом в папку
allure-<версия>/. Если Allure уже есть в PATH или папка уже существует,
ничего не делает. Требуется подключение к интернету и (для работы Allure)
установленная Java 8+.
"""
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import zipfile

ALLURE_VERSION = os.environ.get('ALLURE_VERSION', '2.30.0')
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ALLURE_DIR = os.path.join(PROJECT_DIR, f'allure-{ALLURE_VERSION}')
BASE_URL = (
    'https://github.com/allure-framework/allure2/releases/download/'
    f'{ALLURE_VERSION}/allure-{ALLURE_VERSION}'
)
IS_WINDOWS = sys.platform.startswith('win')


def allure_available():
    """Allure уже установлен (в PATH или папке проекта)?"""
    if shutil.which('allure'):
        return True
    if IS_WINDOWS and shutil.which('allure.bat'):
        return True
    return os.path.isdir(ALLURE_DIR)


def download_with_urllib(url, dest):
    """Скачать файл через стандартную библиотеку Python."""
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request, timeout=120) as response, \
            open(dest, 'wb') as out:
        shutil.copyfileobj(response, out)


def download_with_system_tool(url, dest):
    """Скачать файл системным инструментом (запасной вариант)."""
    if IS_WINDOWS:
        powershell = (
            '[Net.ServicePointManager]::SecurityProtocol = '
            '[Net.SecurityProtocolType]::Tls12; '
            f"Invoke-WebRequest -Uri '{url}' -OutFile '{dest}' -UseBasicParsing"
        )
        subprocess.run(
            ['powershell', '-NoProfile', '-Command', powershell], check=True
        )
    else:
        tool = shutil.which('wget') or shutil.which('curl')
        if not tool:
            raise RuntimeError(
                'Не найден инструмент для скачивания ' +
                '(нужен wget или curl, либо включённый TLS в Python)'
            )
        if os.path.basename(tool).startswith('wget'):
            subprocess.run([tool, '-q', url, '-O', dest], check=True)
        else:
            subprocess.run([tool, '-sSL', url, '-o', dest], check=True)


def download_file(url, dest):
    """Скачать файл, при сбое — повторить системным инструментом."""
    try:
        download_with_urllib(url, dest)
    except Exception as exc:
        print(f'Не удалось скачать через urllib ({exc}); пробую системный инструмент...')
        download_with_system_tool(url, dest)


def extract(archive, dest_dir):
    """Распаковать архив в указанную папку."""
    if archive.endswith('.zip'):
        with zipfile.ZipFile(archive) as z:
            z.extractall(dest_dir)
    else:
        with tarfile.open(archive, 'r:gz') as t:
            t.extractall(dest_dir)


def main():
    if os.path.isdir(ALLURE_DIR):
        print(f'Allure уже установлен в {ALLURE_DIR}')
        return 0
    if allure_available():
        print('Allure уже доступен в PATH — дополнительно ничего не нужно.')
        return 0

    filename = f'allure-{ALLURE_VERSION}.zip' if IS_WINDOWS \
        else f'allure-{ALLURE_VERSION}.tgz'
    url = f'{BASE_URL}/{filename}'
    print(f'Устанавливаю Allure {ALLURE_VERSION}...')

    with tempfile.TemporaryDirectory() as tmp:
        archive_path = os.path.join(tmp, filename)
        download_file(url, archive_path)
        extract(archive_path, tmp)
        extracted = os.path.join(tmp, f'allure-{ALLURE_VERSION}')
        shutil.move(extracted, ALLURE_DIR)

    print('\nAllure CLI установлен. Запуск отчёта:')
    if IS_WINDOWS:
        print(f'  {os.path.join(ALLURE_DIR, "bin", "allure.bat")} serve allure_results')
    else:
        print(f'  {os.path.join(ALLURE_DIR, "bin", "allure")} serve allure_results')
    return 0


if __name__ == '__main__':
    sys.exit(main())
