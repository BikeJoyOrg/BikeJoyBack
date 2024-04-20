# BikeJoyBack instruccions
python -m venv env

env/Scripts/activate

pip install -r requirements.txt

- per activar server s'ha d'estar al directori on hi hagi el fitxer "manage.py"
  
python manage.py runserver

- per acutalitzar taules s'ha d'estar al directori on hi hagi el fitxer "manage.py"
  
python manage.py migrate

python manage.py makemigrations "nomapp"

--------
python manage.py startapp "nomApp"

prova ci cd9
