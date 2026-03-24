# ==============================
# Settings
# ==============================
IMAGE=flavel/nhl_project
TAG=latest
CONTAINER=nhl_parser

# ==============================
# Build Docker image
# ==============================
build:
	docker build -t $(IMAGE):$(TAG) .

# ==============================
# Run container (Django)
# ==============================
run:
	docker run -d -p 8000:8000 --name $(CONTAINER) $(IMAGE):$(TAG)

# ==============================
# Stop container
# ==============================
stop:
	docker stop $(CONTAINER) || true
	docker rm $(CONTAINER) || true

# ==============================
# Restart container (update)
# ==============================
restart: stop run

# ==============================
# View logs
# ==============================
logs:
	docker logs -f $(CONTAINER)

# ==============================
# Run update_data.py inside container
# ==============================
update:
	docker exec -it $(CONTAINER) python myproject/update_data.py

# ==============================
# Push image to Docker Hub
# ==============================
push:
	docker push $(IMAGE):$(TAG)

# ==============================
# Full cycle: build, stop, run
# ==============================
all: build stop run
