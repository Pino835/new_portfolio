# Portafolio Django — Juan Diego Pino Torres

Registro vivo del proyecto. Actualizar esta guía conforme se hagan cambios relevantes.

## Qué es

Portafolio profesional personal (perfil de TI) construido con Django 6.0, desplegado en Render:
https://juan-diego-pino-portfolio.onrender.com

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
    └── media/projects/       # imágenes de los 10 proyectos (versionadas, ver Cambios cuarta tanda)
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

- Plataforma: **Render**. Servicio anterior (`new-portfolio-c8yq.onrender.com`) fue eliminado por el usuario; nuevo servicio planeado con nombre `juan-diego-pino-portfolio` (dominio final: `juan-diego-pino-portfolio.onrender.com`).
- `ALLOWED_HOSTS` se lee de la variable de entorno `ALLOWED_HOSTS` (lista separada por comas), default actualizado a `localhost,127.0.0.1,juan-diego-pino-portfolio.onrender.com`.
- Estáticos servidos con **Whitenoise** (`whitenoise.middleware.WhiteNoiseMiddleware` + `CompressedManifestStaticFilesStorage`).
- `MEDIA_ROOT`/`MEDIA_URL` configurados (`portfolio/media/`). Las imágenes de los 10 proyectos ya están versionadas en git (`media/projects/`, ver tanda anterior) así que sobreviven a redeploys; solo los uploads *nuevos* vía admin se seguirían perdiendo por el filesystem efímero.
- **Build/deploy ahora versionado en código** (`build.sh` + `render.yaml` en la raíz del repo) en vez de vivir solo en el dashboard — ver sección siguiente.
- Base de datos: **SQLite por decisión explícita del usuario** (por ahora). Los proyectos cargados desde el admin en producción se perderán en cada redeploy hasta que se migre a Postgres — queda documentado como pendiente, no como bug urgente.

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

## Cambios ya aplicados (2026-09-05, tercera tanda — SEO y Open Graph)

- Agregados meta tags Open Graph (`og:type`, `og:title`, `og:description`, `og:image`, `og:url`, `og:locale`) y Twitter Card (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`) en `index.html`, usando `profile.jpg` como imagen. Las URLs se construyen dinámicamente con `{{ request.scheme }}://{{ request.get_host }}` para que funcionen igual en local y en producción sin hardcodear el dominio.
- Agregado `robots.txt` (`core/templates/robots.txt`) y `sitemap.xml` (`core/templates/sitemap.xml`) servidos vía `TemplateView` con `content_type` correcto (`core/views.py`: `RobotsTxtView`, `SitemapXmlView`), registrados en `portfolio/urls.py` en `/robots.txt` y `/sitemap.xml`. `robots.txt` bloquea `/admin_portfolio_jdp/` y apunta al sitemap.
- Verificado en local: ambos endpoints responden 200 con contenido correcto y URLs absolutas dinámicas.

## Cambios ya aplicados (2026-09-05, cuarta tanda — limpieza CSS/JS, bug de imágenes y optimización)

- Eliminado código muerto de analytics en `main.js` (`trackEvent`/`gtag`): nunca se ejecutaba porque Google Analytics no estaba cargado en el HTML. Decisión: eliminar en vez de completar la integración (no había GA4 real que conectar).
- Movidos todos los `style="..."` inline de `index.html` a clases nuevas en `style.css` (`.hero-description-muted`, `.section-subtitle`, `.project-image-placeholder`, `.projects-empty`, `.contact-message-action`), reutilizando las variables de color existentes (`--text-muted`, `--primary-cyan`, etc.) en vez de repetir hex codes.
- **Bug encontrado y corregido**: las imágenes de los 10 proyectos (`Project.image`) apuntaban a `projects/*.png` relativo a `MEDIA_ROOT`, pero los archivos reales vivían en `portfolio/projects/` (fuera de `MEDIA_ROOT`, que ahora es `portfolio/media/`) — daban 404 tanto en local como probablemente en producción. Se movieron a `portfolio/media/projects/` (coincide con las rutas ya guardadas en la BD, no hizo falta tocar los registros).
- Al mover las imágenes se aprovechó para comprimirlas: redimensionadas a máx. 1200px de ancho (eran ~1900px) y reoptimizadas como PNG. Total: 5.87MB → 2.89MB (~51% menos), sin pérdida visible de calidad.
- `.gitignore` ajustado: `media/` se ignora en general (para uploads futuros vía admin) pero con excepción explícita `!media/projects/` — estas imágenes son contenido fijo del sitio (no uploads de usuario) y deben persistir en cada deploy de Render, ya que el filesystem ahí es efímero.
- Verificado en local: `manage.py check` limpio, tests 5/5 OK, imagen de proyecto responde 200 en `/media/projects/portafolio.png`.

## Cambios ya aplicados (2026-09-05, quinta tanda — nuevo servicio en Render)

- El usuario eliminó el servicio anterior de Render y creará uno nuevo. Preparado el repo para deploy reproducible por código:
  - `build.sh` (raíz): instala dependencias, corre `collectstatic` y `migrate`.
  - `render.yaml` (raíz): define el web service (`juan-diego-pino-portfolio`, plan free, runtime Python), build/start command, y env vars (`SECRET_KEY` autogenerado, `DEBUG=False`, `ALLOWED_HOSTS`).
  - `gunicorn==26.2.0` agregado a `requirements.txt` (servidor WSGI de producción; no se puede probar en Windows local por depender de `fcntl`, pero Render corre Linux).
  - `ALLOWED_HOSTS` default en `settings.py` actualizado al nuevo dominio esperado.
- **Servicio creado y publicado por el usuario**: https://juan-diego-pino-portfolio.onrender.com — Blueprint funcionó correctamente con el nombre esperado (`ALLOWED_HOSTS` no necesitó ajuste).

## Cambios ya aplicados (2026-09-05, sexta tanda — bug de media en producción real)

- **Bug encontrado en producción** (no se detectaba en local con `runserver` + `DEBUG=True`): con `DEBUG=False`, Django deja de servir `MEDIA_ROOT` vía `urls.py` (ese bloque solo se activa `if settings.DEBUG`), y Whitenoise por defecto solo sirve `STATIC_ROOT`, no `MEDIA_ROOT`. Resultado: todas las imágenes de proyectos daban 404 en el sitio publicado (`/media/projects/*.png`), aunque en local con `DEBUG=True` se veían bien.
- Solución: `core/middleware.py` define `MediaWhiteNoiseMiddleware`, una subclase de `WhiteNoiseMiddleware` que además registra `MEDIA_ROOT` con `add_files(..., prefix=MEDIA_URL)` en su `__init__`. Reemplaza a `whitenoise.middleware.WhiteNoiseMiddleware` en `MIDDLEWARE` (`settings.py`). Justificación: las imágenes de proyectos son contenido fijo versionado en git, no uploads dinámicos, así que tiene sentido servirlas igual que los estáticos.
- Verificado localmente simulando producción (`DEBUG=False python manage.py runserver`): `/`, `/static/css/style.css`, `/static/images/favicon.ico` y `/media/projects/portafolio.png` responden 200. Tests 5/5 OK.
- **Importante**: si en el futuro se agregan uploads dinámicos reales vía admin (no solo estas 10 imágenes fijas), este middleware seguiría sirviéndolos también — pero recordar que en Render el filesystem es efímero, así que un upload nuevo se serviría hasta el próximo restart/deploy y luego desaparecería (ver punto de Postgres/S3 pendiente abajo).

## Cambios ya aplicados (2026-09-05, séptima tanda — reposicionamiento profesional)

El usuario cambió de foco profesional: ya no se presenta como "Full-Stack Developer / Especialista en Ciberseguridad", sino como profesional que dirige herramientas de IA (Claude, Claude Code) para construir, auditar y documentar software real, aplicando buenas prácticas de TI. Contexto: tiene un trabajo actual no técnico (Auxiliar Administrativo) donde, por iniciativa propia, construyó automatizaciones internas usando IA.

- **Hero/tagline**: cambiado de "Full-Stack Developer | Especialista en Ciberseguridad" a "Desarrollo y Automatización Asistidos por IA". Se decidió explícitamente NO mencionar Ciberseguridad en el tagline principal (sigue apareciendo en experiencia/habilidades como parte de su trayectoria, pero no como foco actual).
- **Sección Sobre Mí**: reescrita para reflejar el nuevo enfoque (dirige herramientas de IA como parte del flujo de trabajo, no busca roles de desarrollador tradicional).
- **Nueva experiencia laboral** (primera en la lista, la más reciente): Auxiliar Administrativo, Grupo Inteca / Mercasa, jul. 2026 - Presente. Describe 4 logros/proyectos de automatización hechos con IA como parte de ese rol.
- **4 proyectos nuevos agregados a la base de datos** (`order` -4 a -1, para que aparezcan primero que los 10 existentes): Renombrador de Documentos por Contenido, Robot Clasificador de Documentos con IA (Claude API + SQL Server + SharePoint), Módulo de Logs para Robot Clasificador (.NET + Angular), Renombrador de Archivos Configurable. Son proyectos internos de la empresa — sin repos/demos públicos por confidencialidad, solo descripción y tecnologías.
- **Habilidades**: agregado Claude, Claude Code (sección IA) y Angular (sección Frameworks & Backend).
- **Email corregido**: de `pino2002@gmail.com` (typo introducido en una tanda anterior) a `pinoto2002@gmail.com` (el correcto, confirmado contra el CV real del usuario).
- **CTA de contacto**: cambiado de "disponible para nuevas oportunidades como Full Stack Developer o Security Analyst" a "abierto a colaborar en proyectos de automatización, desarrollo asistido por IA o consultoría" — ya no busca empleo activamente (tiene trabajo actual).
- Meta tags (`<title>`, `description`, `keywords`, Open Graph, Twitter Card) y footer actualizados al nuevo posicionamiento ("Profesional en Informática" en vez de "Ingeniero Informático").
- **Dato importante de esta sesión**: al crear los 4 proyectos nuevos vía `manage.py shell -c "..."` en Git Bash/Windows, los caracteres acentuados (á, é, í, ó, ú) se corrompieron en SQLite por un problema de codepage de la terminal (no de Django/SQLite). Hubo que corregir escribiendo el contenido a un archivo `.py` en UTF-8 y ejecutándolo con `exec(open(..., encoding='utf-8').read())` dentro del shell. **Para cualquier alta de datos futura con texto acentuado desde este entorno de terminal, usar ese patrón (archivo + exec), nunca `-c` inline con acentos.**
- Verificado en local: `manage.py check` limpio, tests 5/5 OK, títulos y descripciones con encoding correcto confirmados vía archivo (no vía stdout de la terminal, que los muestra mal aunque estén bien guardados).

## Problemas conocidos / deuda técnica (pendientes)

1. **Persistencia de datos dinámicos en Render**: SQLite + filesystem efímero implica pérdida de proyectos nuevos cargados vía admin (y de imágenes subidas ahí) en cada deploy/restart. Las imágenes de los 10 proyectos actuales ya están resueltas (versionadas en `media/projects/`, servidas por `MediaWhiteNoiseMiddleware`), pero cualquier proyecto **nuevo** agregado desde el admin en producción se perderá. Recomendado a futuro: Postgres (Render lo ofrece gratis) + storage externo (S3/Cloudinary) para uploads dinámicos.
2. Ruta de admin personalizada (`/admin_portfolio_jdp/`) — está bien como medida de oscurecimiento, pero no reemplaza autenticación fuerte.
3. `og:image` usa `profile.jpg` (800x800, cuadrada) en vez de un banner 1200x630 dedicado — mejora opcional, no urgente.

## Convenciones / notas

- El usuario prefiere trabajar en español; todos los mensajes de commit existentes están en español y numerados ("Commit #10: ...").
- Proyecto pequeño, una sola app (`core`) — evitar sobre-ingeniería (no crear apps adicionales innecesarias, no añadir abstracciones no pedidas).
