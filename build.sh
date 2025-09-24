#!/bin/bash
set -x  # ← MUESTRA CADA COMANDO EN EL LOG

echo "🔧 INICIA BUILD.SH"
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

echo "📊 Ejecutando migraciones..."
python manage.py migrate

echo "📥 Cargando datos iniciales..."
python manage.py loaddata db.json

echo "👤 Creando superusuario..."
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pixelogic.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@pixelogic.com', 'admin123')
    print('✅ Superusuario admin creado')
else:
    print('ℹ️ Usuario admin ya existe')
"

echo "📦 Recolectando estáticos..."
python manage.py collectstatic --noinput

echo "✅ BUILD.SH TERMINADO"