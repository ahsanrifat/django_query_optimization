echo "Waiting for postgres to start"
./wait-for db:5432

# echo "Migrate the database"
# python3 manage.py makemigrations && python manage.py migrate

# echo "Starting the server"
# python3 manage.py runserver 0.0.0.0:8000