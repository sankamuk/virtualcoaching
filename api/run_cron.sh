export FLASK_CONFIG=development

cd __APP-HOME__/examnow/api
source ./venv/bin/activate

if [ $1 == "15minutes" ]
then
	python 15minutes_jobs.py > 15minutes_jobs.log 2>&1
elif [ $1 == "hourly" ]
then
        python hourly_jobs.py > hourly_jobs.log 2>&1
fi
