#!/usr/bin/env bash
# build.sh - Script de construcción robusto para Render

set -e
set -x

echo "🔧 INICIA BUILD.SH"

pip install -r requirements.txt

echo "🌐 Obteniendo datos de producción..."
DATA_URL="https://raw.githubusercontent.com/andresgorena1079-dot/pixelogic-sin-fronteras/main/datos_produccion_final.json"
FILENAME="datos_produccion_final.json"
curl -L -o $FILENAME $DATA_URL
echo "✅ Archivo de datos descargado."

# Aseguramos que los comandos de manage.py usen las settings de producción
export DJANGO_SETTINGS_MODULE=pixelogic.prod_settings

echo "📊 Aplicando migraciones..."
python manage.py migrate

echo "🧹 Limpiando la base de datos (flush)..."
python manage.py flush --no-input
echo "✅ Base de datos limpia."

echo "📥 Cargando datos desde '$FILENAME'..."
python manage.py loaddata $FILENAME
echo "✅ Datos cargados exitosamente."

echo "👤 Creando superusuario..."
python create_superuser.py # Usamos el script dedicado

echo "🎨 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ BUILD.SH TERMINADO"