# primero ejecutar esto para que nos de una consola virtual
# python manage.py shell


from django.db import connection

cursor = connection.cursor()
cursor.execute("DELETE FROM django_migrations;")
connection.commit()
exit()
