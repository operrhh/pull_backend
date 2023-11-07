# Usar una imagen base oficial de Python
FROM python:3.10

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias del sistema para Oracle
RUN apt-get update \
    && apt-get install -y --no-install-recommends libaio1 wget unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Descargar e instalar el cliente instantáneo de Oracle
RUN mkdir -p /opt/oracle \
    && cd /opt/oracle \
    && wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip \
    && unzip instantclient-basiclite-linuxx64.zip \
    && rm -f instantclient-basiclite-linuxx64.zip \
    && mv instantclient_*/ . \
    && rmdir instantclient_* \
    && sh -c "echo /opt/oracle > /etc/ld.so.conf.d/oracle-instantclient.conf" \
    && ldconfig

# Instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . /app/

# Recoger archivos estáticos
RUN python manage.py collectstatic --noinput

# Comando para ejecutar la aplicación
CMD ["gunicorn", "-b", "0.0.0.0:8000", "integraSoft_rest.wsgi:application"]
