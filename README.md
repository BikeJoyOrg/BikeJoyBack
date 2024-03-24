# BikeJoyBack instruccions
python -m venv env

env/Scripts/activate

pip install django

pip install djangorestframework

pip install django-cors-headers

pip install djongo

pip install dnspython

pip install pymongo==3.12.0


- per activar server s'ha d'estar al directori on hi hagi el fitxer "manage.py"
  
python manage.py runserver

- per acutalitzar taules s'ha d'estar al directori on hi hagi el fitxer "manage.py"
  
python manage.py migrate

python manage.py makemigrations "nomapp"

--------
python manage.py startapp Rutes 
