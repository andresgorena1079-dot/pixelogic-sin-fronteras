#!/usr/bin/env bash
# build.sh

# Salir inmediatamente si un comando falla
set -e

# Mostrar cada comando en el log
set -x

echo "🔧 INICIA BUILD.SH"

# 1. Instalando dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# 2. Descargando el archivo de datos de producción
echo "🌐 Obteniendo datos de producción..."
# --- URL CORREGIDA ---
DATA_URL="https://raw.githubusercontent.com/andresgorena1079-dot/pixelogic-sin-fronteras/main/datos_produccion_final.json"
FILENAME="datos_produccion_final.json"
curl -L -o $FILENAME $DATA_URL
echo "✅ Archivo de datos descargado como '$FILENAME'."

# 3. Ejecutando migraciones
echo "📊 Aplicando migraciones a la base de datos..."
python manage.py migrate

# 4. Limpiando la base de datos antes de cargar datos nuevos (opcional pero recomendado)
echo "🧹 Limpiando la base de datos (flush)..."
python manage.py flush --no-input
echo "✅ Base de datos limpia."

# 5. Cargando los datos iniciales
echo "📥 Cargando datos desde '$FILENAME'..."
python manage.py loaddata $FILENAME
echo "✅ Datos cargados exitosamente."

# 6. Creando superusuario (de forma segura)
echo "👤 Creando superusuario..."
# Asegúrate que las settings de producción se usen aquí también
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pixelogic.prod_settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@pixelogic.com', 'admin123')
    print('✅ Superusuario admin creado.')
else:
    print('ℹ️ Superusuario admin ya existe.')
"

# 7. Recolectando estáticos
echo "🎨 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ BUILD.SH TERMINADO"