# Сравниваем вакансии программистов

Сервис используется для сравнения зарплат вакансий программистов в Москве,
размещённых на сайтах [HeadHunter](https://hh.ru) и [SuperJob](https://www.superjob.ru).

## Как установить
1. Нужно зарегистрироваться на сайте [SuperJob](https://api.superjob.ru/) и получить API key.
2. Полученные данные присвоить переменной окружения в файле ".env".

```python
API_KEY_SUPERJOB=ВАШ_API_key
```

3. Установить зависимости.

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
Рекомендуется использовать [virtualenv/env](https://docs.python.org/3/library/venv.html) для изоляции проекта.

## Как использовать

Для использования сервиса необходимо запустить:

```
python fetch_vacancies.py
```

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
