#!/bin/bash
set -o errexit

echo "📦 Instalando dependencias..."
pip install -r requirements.txt

echo "📊 Aplicando migraciones..."
python manage.py migrate

echo "📥 Cargando datos iniciales..."
python manage.py loaddata db.json

echo "👤 Creando superusuario..."
python create_superuser.py

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Build completado"