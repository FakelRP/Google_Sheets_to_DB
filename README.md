Google Sheets document - https://docs.google.com/spreadsheets/d/1ZxzdUub2mT-Ch-bJ-c0XqdxeWwzk8_3eQZEtZhT2Te0/edit?usp=sharing

Инструкция по запуску:
1. Создать новый проект в IDE c venv
2. Клонировать репозиторий к себе - git clone https://github.com/FakelRP/Google_Sheets_to_DB.git
3. Установить все необходимые библиотеки - pip instal requirements.txt
4. Создать базу данных (я создал через pgAdmin4) 
5. Создать таблицу в базе данных со следующим SQL запросом - CREATE TABLE orders ("№" int, "заказ_№" int, "стоимость_$" int, "срок_поставки" text, "стоимость_руб" text)
6. Запустить скрипт (main.py)

Скрипт работает постоянно, каждые 15 секунд обновляя данные в БД.
