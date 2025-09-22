python manage.py runserver
http://127.0.0.1:8000/cuentas/registro/ 
http://127.0.0.1:8000/admin
http://127.0.0.1:8000


#abrir consola de google cloud
https://console.cloud.google.com


#para migrar todo
python manage.py makemigrations
python manage.py migrate


#crear super usuario
python manage.py createsuperuser

from django.db import connection
cursor = connection.cursor()
cursor.execute("DELETE FROM django_migrations;")
connection.commit()
exit()




