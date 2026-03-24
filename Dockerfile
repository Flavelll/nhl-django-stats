# ==============================
# Dockerfile for Django + SQLite
# ==============================

FROM python:3.12-slim

# ==============================
# Set working directory
# ==============================
WORKDIR /app

# ==============================
# Install sqlite3
# ==============================
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# ==============================
# Copy Django project
# ==============================
COPY ./myproject ./myproject

# ==============================
# Install Python requirements
# ==============================
RUN pip install --no-cache-dir -r ./myproject/requirements.txt

# ==============================
# Initialize SQLite database:
# - run init.sql
# - import CSV files
# ==============================
RUN sqlite3 db.sqlite3 <<EOF
.read ./myproject/nhl_app/scripts/init.sql
.separator ","
.mode csv
.import --skip 1 ./myproject/nhl_app/data/boxscore.csv bx
.import --skip 1 ./myproject/nhl_app/data/story.csv story
EOF

# ==============================
# Apply Django migrations
# ==============================
RUN python myproject/manage.py migrate

# ==============================
# Expose port for Django
# ==============================
EXPOSE 8000

# ==============================
# Start Django development server
# ==============================
CMD ["python", "myproject/manage.py", "runserver", "0.0.0.0:8000"]
