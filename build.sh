#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

cd portfolio
python manage.py collectstatic --noinput
python manage.py migrate

# Carga los proyectos iniciales solo si la tabla esta vacia (no duplica en
# builds siguientes).
python manage.py seed_projects

# Crea el superusuario del admin si no existe todavia. Requiere las env vars
# DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL y DJANGO_SUPERUSER_PASSWORD
# configuradas en el dashboard de Render (nunca en el codigo). Si ya existe un
# usuario con ese username, Django no hace nada (no falla el build).
if [[ -n "$DJANGO_SUPERUSER_USERNAME" ]]; then
  python manage.py createsuperuser --noinput || true
fi
