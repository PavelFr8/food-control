# food-control

Что делает пайплайн?

- Проверяет код через flake8 и black
- Проверяет, что все тесты прошли

---

## Требования

- Python версии 3.9+
- Установленный Git
- Установленные зависимости из `requirements/dev.txt`

---

## Туториал по запуску приложения в dev-режиме

### Клонирование репозитория

```bash
git clone https://github.com/PavelFr8/food-control
cd food-control
```

### Создание виртуальной среды

```bash
python3 -m venv venv
```

### Запуск виртуальной среды

Для Linux/Mac:

```bash
source venv/bin/activate
```

Для Windows:

```bash
venv\Scripts\activate
```

### Загрузка библиотек

```bash
pip install -r requirements/dev.txt
```

### Задание переменных окружения

Скопируйте файл с примером переменных окружения:

Для Linux/Mac:

```bash
cp template.env .env
```

Для Windows:

```bash
copy template.env .env
```

**Примечание:** Не забудьте изменить значения переменных в `.env` в соответствии с вашими настройками.

### Перенос миграций

Перенесите миграции в базу данных:

```bash
cd food_control
python3 manage.py migrate
```

По желанию вы можете добавить в БД тестовые данные от разработчика:

```bash
python3 manage.py loaddata fixtures/data.json
```

### Тестирование

Для проверки правильности настройки приложения вы можете запустить тестирование

```bash
python3 manage.py test
```

### Создание супер-пользователя

Для проверки работы админки рекомендуется создать супер-пользователя. (После ввода команд нужно будет минимум придумать и ввести пароль)

```bash
python3 manage.py createsuperuser
```

### Запуск сервера

```bash
python3 manage.py runserver
```

---

## ER-диаграммы базы данных


На данный момент отсутствуют