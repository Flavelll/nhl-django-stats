
# NHL Stats Django Project

A simple Django project for collecting and analyzing NHL statistics via API.

## ⚡ Features

- Fetch NHL games data (regular season + playoffs)
- Incremental updates (fetch only new games)
- Store data in SQLite
- Web interface using Django
- Dockerized for easy deployment

## 📂 Project Structure

```

├── Dockerfile              # Docker image build
├── Makefile                # Docker + update commands
└── myproject
├── config
│   └── settings.py     # Django settings
├── manage.py           # Django CLI
├── nhl_app             # NHL stats app
│   ├── data            # batch CSV data
│   ├── forms.py        # forms
│   ├── queries.py      # helper queries
│   ├── templates       # HTML templates
│   ├── urls.py         # routing
│   └── views.py        # views
├── requirements.txt    # Python dependencies
├── static
│   ├── css
│   └── js
├── stats_app           # homepage app
└── update_data.py      # incremental update script

````

## 🛠️ Makefile Commands

| Command      | Description                                      |
|--------------|--------------------------------------------------|
| `make build` | Build the Docker image                           |
| `make run`   | Run the Django server in Docker                  |
| `make stop`  | Stop and remove the container                    |
| `make restart` | Restart the container                           |
| `make logs`  | View container logs                               |
| `make update` | Run the data update script inside the container |

## 🚀 Access

- Default host: `0.0.0.0`
- Default port: `8000`

Open in browser: http://localhost:8000

## 💡 Notes

- The SQLite database (`db.sqlite3`) is created automatically by Django migrations.
- Incremental updates check the last game ID in the database to avoid duplicates.
- Docker makes it easy to run the project on any system without local setup.
- API requests have a small delay (`SLEEP_BETWEEN`) to avoid overloading NHL servers.

## 🐳 Docker Hub

```bash
docker pull flavel/nhl_project:latest
````

