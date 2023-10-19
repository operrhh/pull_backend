#!/bin/bash

# Cambiar al directorio del proyecto
cd /home/integrasoft/Backend/backend/integrasoft

# Activar el entorno virtual
source /home/integrasoft/Backend/virtual-backend/bin/activate

# Obtener los últimos cambios del repositorio
git pull origin main

# Desactivar el entorno virtual si es necesario
deactivate
