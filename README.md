# capitan
Docker Web UI

Initialize with:
docker-compose up web
docker exec -it <container_id> bash

export FLASK_APP=/capitan/capitan/autoapp.py
flask initdb


Start with:

docker-compose up web
