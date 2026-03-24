# ==============================
# Dockerfile для Django + SQLite
# ==============================

FROM python:3.12-slim

# ==============================
# Робоча директорія
# ==============================
WORKDIR /app

# ==============================
# Установка sqlite3 та інших утиліт
# ==============================
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# ==============================
# Копіюємо Django-проєкт
# ==============================
COPY ./myproject ./myproject

# ==============================
# Встановлюємо залежності Python
# ==============================
RUN pip install --no-cache-dir -r ./myproject/requirements.txt

# ==============================
# Міграції Django + імпорт CSV + init_sqlite.sql
# ==============================

RUN sqlite3 db.sqlite3 <<EOF
.read ./myproject/nhl_app/scripts/init.sql
.separator ","
.mode csv
.import --skip 1 ./myproject/nhl_app/data/boxscore.csv bx
.import --skip 1 ./myproject/nhl_app/data/story.csv story
EOF

RUN python myproject/manage.py migrate
# ==============================
# Збір статичних файлів
# ==============================
# RUN python myproject/manage.py collectstatic --noinput

# ==============================
# Порт для Django
# ==============================
EXPOSE 8000

# ==============================
# CMD для запуску сервера
# ==============================
CMD ["python", "myproject/manage.py", "runserver", "0.0.0.0:8000"]
