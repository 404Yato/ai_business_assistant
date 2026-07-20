#!/bin/sh
set -e

mkdir -p /var/lib/odoo
chown -R odoo:odoo /var/lib/odoo
chmod -R 755 /var/lib/odoo

cat >/etc/odoo/odoo.conf <<EOF
[options]
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
data_dir = /var/lib/odoo

db_host = ${PGHOST}
db_port = ${PGPORT}
db_user = ${PGUSER}
db_password = ${PGPASSWORD}
db_name = ${PGDATABASE}

http_interface = 0.0.0.0
http_port = 8069
proxy_mode = True
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


echo "PostgreSQL disponible."


INITIALIZED=$(PGPASSWORD="$PGPASSWORD" psql \
    -h "$PGHOST" \
    -p "$PGPORT" \
    -U "$PGUSER" \
    -d "$PGDATABASE" \
    -tAc "SELECT COUNT(*) FROM pg_tables WHERE schemaname='public' AND tablename='ir_module_module';")


if [ "$INITIALIZED" = "1" ]; then
    echo "Base de datos ya inicializada."

    exec odoo \
        --http-interface=0.0.0.0 \
        --http-port=8069

else
    echo "Inicializando Odoo..."

    exec odoo \
        --http-interface=0.0.0.0 \
        --http-port=8069 \
        -d "$PGDATABASE" \
        -i base \
        --without-demo=all
fi