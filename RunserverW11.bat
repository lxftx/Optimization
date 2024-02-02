@echo off

cd C:\optimization

rem Создание виртуального окружения
py -m venv venv

rem Активация виртуального окружения (если используется)
call C:\optimization\venv\Scripts\activate

rem Установка необходимых библиотек
pip install -r requirements.txt

rem Переход в директорию с вашим Django проектом
cd C:\optimization\siteoptimization

rem Запуск миграций (если необходимо)
py manage.py makemigrations
py manage.py migrate

rem Запуск сервера Django
py manage.py runserver

pause