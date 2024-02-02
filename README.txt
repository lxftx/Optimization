1) Директорию optimization добавляем на диск С
2) Для запуска локального сервера используем файл в зависимости от версии Windows, для windows 10 и меньше - RunserverW10.bat или
для windows11 - RunserverW11.bat.

Содержимое файла Runserver.bat:

"@echo off

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

pause"

3) После запуска файла Runserver.bat, создается виртуальное окружение venv в каталоге optimization
4) Скачиваются нужные библиотеки с файла requirements.txt
5) Запускаются миграции
6) Запускается сервер