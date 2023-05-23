This appplication could only be ran on Linux/Mac os
Because some of the django extencions are not compatible with Windows e.g Celery

to start this application firstly we need to install virtual environment and activate it

cd /grc_app/Project_fyp

python3.8 -m venv venv
source venv/bin/activate

then install all requirements

python -m pip install -r requirements.txt

afterwareds we need to create docker instance for redis  Note: it will only work on Linux/Mac os

docker compose up -d

now we need to go to the django application directory
 
cd /src/groceryapp

To start the application:

just in case migrate the tables:

python manage.py makemigrations
python manage.py migrate

Create superuser:

python manage.py createsuperuser

after that we can run the server:

python manage.py runserver

If you want to have dynamic ratings then input this command:

celery -A groceryapp worker --beat --scheduler django --loglevel=info

Celery will run a schejuled job of updating all grocery item ratings every 60 seconds




