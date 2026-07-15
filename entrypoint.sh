#!/bin/sh
set -e

cat >/etc/odoo/odoo.conf <<EOF
[options]
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
data_dir = /var/lib/odoo

db_host = ${HOST}
db_port = ${PORT}
db_user = ${USER}
db_password = ${PASSWORD}
db_name = ${DATABASE}
EOF

echo "Esperando PostgreSQL..."
until PGPASSWORD="$PASSWORD" psql \
    -h "$HOST" \
    -p "$PORT" \
    -U "$USER" \
    -d "$DATABASE" \
    -c "SELECT 1;" >/dev/null 2>&1
do
    sleep 2
done

INITIALIZED=$(PGPASSWORD="$PASSWORD" psql \
    -h "$HOST" \
    -p "$PORT" \
    -U "$USER" \
    -d "$DATABASE" \
    -tAc "SELECT COUNT(*) FROM pg_tables WHERE schemaname='public' AND tablename='ir_module_module';")

if [ "$INITIALIZED" = "1" ]; then
    echo "Base de datos ya inicializada."
    exec odoo
else
    echo "Inicializando Odoo..."
    exec odoo -d "$DATABASE" -i base --without-demo=all
fi