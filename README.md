# Управление спортивным инвентарем в школе

## Состав команды

* Кудинов Павел Дмитриевич ([PavelFr8](https://github.com/PavelFr8))
* Фокин Дмитрий Александрович ([Repdayr](https://github.com/Repdayr))

## Описание проекта

Веб-приложение для учета и контроля школьного спортивного инвентаря. Приложение предоставляет возможность управлять 
инвентарем, отслеживать его состояние, распределять между пользователями, а также планировать закупки.  

## Что делает пайплайн?

- Проверяет код через flake8 и black
- Проверяет, что все тесты прошли

---

## Требования

- Python версии 3.9+
- Установленный Git
- Установленные зависимости из `requirements/dev.txt`

---

## Туториал по запуску приложения в prod-режиме

### Требования

- Установленный Docker и Docker Compose

### Клонирование репозитория

```bash
git clone https://github.com/PavelFr8/food-control
cd food-control
```

### Задание переменных окружения

Скопируйте файл с примером переменных окружения:

Для Linux/Mac:

```bash
cp prod.env .env
```

Для Windows:

```bash
copy prod.env .env
```

### Сборка и запуск веб-приложения

```bash
docker compose up -d --build
```

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
cp dev.env .env
```

Для Windows:

```bash
copy dev.env .env
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
python3 manage.py loaddata fixtures/roles.json
python3 manage.py loaddata fixtures/menu.json
python3 manage.py loaddata fixtures/users.json
python3 manage.py loaddata fixtures/preffs.json
python3 manage.py loaddata fixtures/payments.json
python3 manage.py loaddata fixtures/meals.json
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

![db](docs/db.svg)