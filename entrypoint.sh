#!/bin/sh

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

exec odoo