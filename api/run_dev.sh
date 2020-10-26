export FLASK_CONFIG=development

cd __APP-HOME__/examnow/api
source ./venv/bin/activate

gunicorn --workers=2 --threads=2 --bind 0.0.0.0:__PORT__ run:gapp
