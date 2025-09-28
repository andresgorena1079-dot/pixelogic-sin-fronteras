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


#Para ver el servidor en render
https://pixelogic-sin-fronteras.onrender.com/admin


#Para ver el servidor en render
https://dashboard.render.com/web/srv-d38a0abe5dus73a0f6kg

#Repositorio en github
https://github.com/andresgorena1079-dot/pixelogic-sin-fronteras

# para entrar a cloudinary
https://console.cloudinary.com/app/c-0b2920eb98e86a7996f35ae6eb1c6a/assets/media_library/search?q=&view_mode=mosaic

# para entrar a google search console
https://search.google.com/search-console?resource_id=https%3A%2F%2Fpixelogic-sin-fronteras.onrender.com%2F