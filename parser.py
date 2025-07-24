from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
import requests
import time
import random
from settings import URL, DOC
'''
Настройка браузера
ChromeOptions - класс, который позволяет контролировать поведение
браузера через аргументы командной строки, экспериментальные настройки и другие параметры
'''


def parser():
    options = webdriver.ChromeOptions()
    options.add_argument(
        "--headless")  # запуск без графического интерфейса, в данном случае нужен для экономии ресурсов
    driver = webdriver.Chrome(options=options)

    URL = 'https://www.memify.ru/'
    driver.get(URL)

    image_urls = set()
    max_attempts = 5
    attempts = 0

    while len(image_urls) < 10 and attempts < max_attempts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Ожидание загрузки

        # Поиск всех изображений
        images = driver.find_elements(By.XPATH, "//figure/a/img")
        for img in images:
            if len(image_urls) >= 10:
                break

            # Извлечение URL из атрибутов
            url = img.get_attribute("src")
            if (url and url.startswith("http") and url not in image_urls
                    and url.endswith(("jpg", "png"))):
                image_urls.add(url)
    input_dir = Path(DOC)
    if not input_dir.exists():
        input_dir.mkdir(parents=True, exist_ok=True)
    selected_image = random.choice(list(image_urls))
    filename = selected_image.split(sep="/")[-1]
    filepath = Path(input_dir, filename)
    try:
        response = requests.get(selected_image)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):  #выгружает файл не сразу в память, а небольшими чанками по 1кб
                f.write(chunk)
    except Exception as e:
        print("Ошибка")

    driver.quit()
    return filepath

img = parser()