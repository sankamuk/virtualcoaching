export FLASK_CONFIG=development

cd __APP-HOME__/examnow/api
source ./venv/bin/activate

gunicorn --workers=2 --threads=2 --bind 127.0.0.1:5000 run:gapp
