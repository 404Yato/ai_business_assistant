#!/bin/sh
set -e

cat >/etc/odoo/odoo.conf <<EOF
[options]
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
data_dir = /var/lib/odoo

db_host = ${PGHOST}
db_port = ${PGPORT}
db_user = ${PGUSER}
db_password = ${PGPASSWORD}
db_name = ${PGDATABASE}

http_port = ${PORT}
EOF


echo "Esperando PostgreSQL..."

until PGPASSWORD="$PGPASSWORD" psql \
    -h "$PGHOST" \
    -p "$PGPORT" \
    -U "$PGUSER" \
    -d "$PGDATABASE" \
    -c "SELECT 1;" >/dev/null 2>&1
do
    sleep 2
done


INITIALIZED=$(PGPASSWORD="$PGPASSWORD" psql \
    -h "$PGHOST" \
    -p "$PGPORT" \
    -U "$PGUSER" \
    -d "$PGDATABASE" \
    -tAc "SELECT COUNT(*) FROM pg_tables WHERE schemaname='public' AND tablename='ir_module_module';")


if [ "$INITIALIZED" = "1" ]; then
    echo "Base de datos ya inicializada."
    exec odoo
else
    echo "Inicializando Odoo..."
    exec odoo -d "$PGDATABASE" -i base --without-demo=all
fi