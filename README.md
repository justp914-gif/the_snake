# Змейка

Учебная игра на Python и Pygame. Змейка растёт, когда съедает яблоко,
переходит на противоположную сторону поля у края и начинает заново при
столкновении с собой или заполнении поля.

## Запуск

Используйте Python 3.12. Из корня проекта выполните:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python the_snake.py
```

На Windows в PowerShell активируйте окружение командой `.\.venv\Scripts\Activate.ps1`.

Управление стрелками. Для выхода закройте окно игры.

## Проверки

```sh
python -m pytest
python -m flake8 the_snake.py
```

Исходная версия указана в приложенном README проекта:
[SosalChupu/the_snake](https://github.com/SosalChupu/the_snake).
Лицензия — [MIT](LICENSE).
