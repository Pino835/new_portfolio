# Portafolio Django — Juan Diego Pino Torres

Registro vivo del proyecto. Actualizar esta guía conforme se hagan cambios relevantes.

## Qué es

Portafolio profesional personal (perfil de TI) construido con Django 6.0, desplegado en Render:
https://new-portfolio-c8yq.onrender.com

Es un sitio de una sola página (`HomeView`, `index.html`) que muestra un CV/perfil y una lista de proyectos, administrable desde el admin de Django.

## Estructura

```
new_portfolio/
├── .gitignore                # en la raíz (corregido)
├── README.md
├── requirements.txt
└── portfolio/                # proyecto Django (raíz real de manage.py)
    ├── .env                  # SECRET_KEY, DEBUG (no versionado)
    ├── manage.py
    ├── portfolio/            # settings del proyecto
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py / asgi.py
    └── core/                 # única app Django
        ├── models.py         # modelo Project
        ├── views.py          # HomeView (TemplateView)
        ├── admin.py          # ProjectAdmin
        ├── templates/index.html
        ├── static/{css,js,img,docs}
        └── migrations/
    └── projects/             # imágenes sueltas de proyectos (png) — no es MEDIA_ROOT actualmente usado
```

## Modelo de datos

`core.models.Project`:
- `title`, `description`, `image` (ImageField → `projects/`), `technologies` (string separado por comas), `github_url`, `demo_url`, `order`, timestamps.
- `get_technologies_list()` parte `technologies` por comas.
- Administrable vía `/admin_portfolio_jdp/` (ruta de admin custom, no `/admin/`).

## Vista

`HomeView` (TemplateView) renderiza `index.html` pasando `projects = Project.objects.all()` (respeta el `order` definido en `Meta.ordering`).

## Cómo correr en local

```powershell
cd portfolio
python manage.py runserver
```
Requiere `portfolio/.env` con `SECRET_KEY` y `DEBUG=True` (ya existe localmente, no se versiona).

Verificado: arranca sin errores (`manage.py check` limpio) y responde 200 en `http://127.0.0.1:8000/`.

## Despliegue

- Plataforma: **Render**, dominio `new-portfolio-c8yq.onrender.com`.
- `ALLOWED_HOSTS` ahora se lee de la variable de entorno `ALLOWED_HOSTS` (lista separada por comas), con default `localhost,127.0.0.1,new-portfolio-c8yq.onrender.com`. En Render, configurar la env var si se agrega un dominio propio.
- Estáticos servidos con **Whitenoise** (`whitenoise.middleware.WhiteNoiseMiddleware` + `CompressedManifestStaticFilesStorage`). En el build de Render hay que correr `python manage.py collectstatic --noinput` (agregar al build command si no está).
- `MEDIA_ROOT`/`MEDIA_URL` configurados (`portfolio/media/`), pero **ojo**: el filesystem de Render es efímero — los archivos subidos vía admin (`Project.image`) se pierden en cada redeploy. Si se quiere persistencia real, considerar un storage externo (S3, Cloudinary) más adelante.
- No hay `Procfile`, `build.sh` ni `render.yaml` en el repo — la configuración de build/start command vive solo en el dashboard de Render. Pendiente: documentar o versionar esos comandos.
- Sigue usando SQLite (`db.sqlite3`) como base de datos, ahora sin versionar en git. En Render con filesystem efímero esto significa que **los datos (proyectos cargados vía admin) no persisten entre deploys** — es la limitación más importante a resolver a futuro (migrar a Postgres, p.ej. Render Postgres free tier).

## Cambios ya aplicados (2026-09-05)

- `.gitignore` movido a la raíz del repo, ampliado (`__pycache__/`, `*.pyc`, `.venv/`, `db.sqlite3`, `staticfiles/`, `media/`, `.env`, editores/SO).
- `db.sqlite3` y todos los `__pycache__/*.pyc` desindexados de git (`git rm --cached`), permanecen en disco.
- `requirements.txt` y `README.md` reescritos de UTF-16 a UTF-8.
- `whitenoise==6.11.0` agregado a `requirements.txt` e instalado.
- `settings.py`: `ALLOWED_HOSTS` ahora viene de env var; agregado `WhiteNoiseMiddleware`; agregado `STATIC_ROOT` + `STORAGES` (`default` y `staticfiles`); agregado `MEDIA_URL`/`MEDIA_ROOT`.
- Verificado en local: `manage.py check` limpio, servidor corre, `/` y `/static/css/style.css` responden 200 con Whitenoise sirviendo los estáticos.

## Cambios ya aplicados (2026-09-05, segunda tanda — bugs del frontend)

- Favicon roto: `index.html` referenciaba `static/images/favicon.ico` sin que existiera. Se generó `core/static/images/favicon.ico` (ícono simple "JD" en cian/magenta, estilo cyberpunk del sitio) con Pillow.
- Email inconsistente en la sección de contacto: el `mailto:` decía `pino8302@gmail.com` mientras el texto visible decía `pino2002@gmail.com`. Unificado a `pino2002@gmail.com` en ambos lugares (tarjeta de contacto y botón "Enviar Mensaje").
- Espacio inválido en el `path` del SVG de GitHub (`2.222v 3.293c0` → `2.222v3.293c0`), duplicado en el header y en la sección de contacto.
- `core/tests.py` estaba vacío (solo boilerplate). Se agregaron pruebas para `HomeView` (200 OK, template correcto, orden de proyectos) y para `Project.get_technologies_list()` / `__str__`.
- **Dato importante para tests/CI**: con `CompressedManifestStaticFilesStorage` (Whitenoise), los tests que rendericen templates con `{% static %}` fallan si no existe el manifest de `staticfiles/`. Hay que correr `python manage.py collectstatic --noinput` antes de `python manage.py test`.

## Problemas conocidos / deuda técnica (pendientes)

1. **Persistencia de datos en Render**: SQLite + filesystem efímero implica pérdida de proyectos/imágenes subidas en cada deploy. Recomendado: Postgres (Render lo ofrece gratis) + storage externo para media si se siguen subiendo imágenes vía admin.
2. **`portfolio/projects/*.png`**: imágenes sueltas en una carpeta que no coincide con `MEDIA_ROOT` — pendiente confirmar si son legado de una versión anterior del modelo (antes de que existiera `Project.image`) y si se pueden eliminar.
3. No hay `render.yaml`/`Procfile` versionado — el build/start command de Render no está documentado en el repo. Falta confirmar que el build command incluya `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`.
4. Ruta de admin personalizada (`/admin_portfolio_jdp/`) — está bien como medida de oscurecimiento, pero no reemplaza autenticación fuerte.
5. **Mejoras pendientes de la siguiente tanda**: falta `robots.txt`/`sitemap.xml` para SEO, meta tags Open Graph/Twitter Card para previews al compartir el link, CSS/JS inline en el HTML que podría moverse a clases, código muerto de `gtag` en `main.js` (referenciado pero nunca cargado — decidir si se agrega GA o se elimina), optimización de imágenes de proyectos.

## Convenciones / notas

- El usuario prefiere trabajar en español; todos los mensajes de commit existentes están en español y numerados ("Commit #10: ...").
- Proyecto pequeño, una sola app (`core`) — evitar sobre-ingeniería (no crear apps adicionales innecesarias, no añadir abstracciones no pedidas).
