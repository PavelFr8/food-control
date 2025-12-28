# -----------------------------------------
# 1. Стадия сборки статики Django
# -----------------------------------------
FROM python:3.11-alpine3.18 AS django-static-builder

# Системные зависимости
RUN apk add --no-cache gcc musl-dev postgresql-dev bash

# Рабочая директория
WORKDIR /app

# Копируем все необходимые файлы
COPY ./food_control .
COPY ./requirements ./requirements
COPY ./entrypoint.sh .


# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements/prod.txt

# Настраиваем переменные окружения Django
ENV DJANGO_SETTINGS_MODULE=food_control.settings
ENV DJANGO_DEBUG=False
ENV PYTHONPATH=/app

# Собираем статику
RUN python manage.py collectstatic --noinput

# -----------------------------------------
# 2. Минимальный Django контейнер для API
# -----------------------------------------
FROM python:3.11-alpine3.18 AS django-api

WORKDIR /app

COPY --from=django-static-builder /app /app

RUN pip install --no-cache-dir -r requirements/prod.txt

EXPOSE 8000

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# -----------------------------------------
# 3. Nginx для отдачи статики
# -----------------------------------------
FROM nginx:1.28.1-alpine AS front

COPY --from=django-static-builder /app/static_dev /data/static

COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
