FROM odoo:18

USER root

RUN apt-get update && \
    apt-get install -y python3-venv && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

RUN python3 -m venv /opt/gemini-env

RUN /opt/gemini-env/bin/pip install --upgrade pip

RUN /opt/gemini-env/bin/pip install --no-cache-dir -r /tmp/requirements.txt

COPY addons /mnt/extra-addons

USER odoo

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]