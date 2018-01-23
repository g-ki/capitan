# capitan
Docker Web UI

Initialize with:

docker-compose up web # or docker exec -t <container_id> bash

docker-compose exec web bash

export FLASK_APP=/capitan/capitan/autoapp.py

flask initdb

cp instance/settings.py.production_example instance/settings.py

vim  instance/settings.py # Set DigitalOcean token

kill -HUP masterpid # to restart web server
