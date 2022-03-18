echo "===========Waiting for postgres to start=============="
sleep 5
sh wait-for db:5432


echo "================Making Migration for the postgres DB=================="
sleep 5
python manage.py makemigrations

echo "=================Migrating the postgres DB===================="
sleep 5
python manage.py migrate

echo "====================Starting the server============================"
sleep 5
python manage.py runserver 0.0.0.0:8000