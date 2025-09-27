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
o
https://pixelogic-sin-fronteras.onrender.cm/admin

git add .
git commit -m "Muevo templates dentro del proyecto para Render"
git push origin main


git add -f full_data.json
git commit -m "Exporta base de datos con UTF-8 válido"
git push origin main


# Prepara todos los archivos
git add .

# Crea el commit final
git commit -m "Versión final lista para despliegue con datos"

# Sube todo a GitHub
git push origin main