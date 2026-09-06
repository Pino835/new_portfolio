from django.conf import settings
from whitenoise.middleware import WhiteNoiseMiddleware


class MediaWhiteNoiseMiddleware(WhiteNoiseMiddleware):
    """Sirve MEDIA_ROOT via Whitenoise ademas de STATIC_ROOT.

    Las imagenes de proyectos son contenido fijo versionado en git (no
    uploads dinamicos de usuario), asi que tiene sentido servirlas igual
    que los estaticos aunque DEBUG=False.
    """

    def __init__(self, get_response=None, settings=settings):
        super().__init__(get_response, settings)
        if settings.MEDIA_ROOT:
            self.add_files(str(settings.MEDIA_ROOT), prefix=settings.MEDIA_URL)
