#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to check if PostgreSQL is ready
function wait_for_postgres() {
  echo "Waiting for PostgreSQL to be ready..."
  while ! nc -z db 5432; do
    sleep 0.1
  done
  echo "PostgreSQL is up and running!"
}

# Wait for PostgreSQL
wait_for_postgres

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# (Optional) Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn aicarttracker.wsgi:application --bind 0.0.0.0:8000




#Explanation of the Script:
#!/bin/bash: Specifies that the script should be run in the Bash shell.
#set -e: Ensures the script exits immediately if any command fails.
#wait_for_postgres Function: Uses nc (netcat) to check if the PostgreSQL service (db as defined in docker-compose.yml) is accepting connections on port 5432.
#python manage.py migrate: Applies Django migrations to set up the database schema.
#exec "$@": Replaces the shell with the command passed to the script (e.g., python manage.py runserver).
