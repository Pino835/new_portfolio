from django.core.management.base import BaseCommand

from core.models import Project

LINKS = {
    'Renombrador de Documentos por Contenido': 'https://github.com/Pino835/renombrador-facturas',
    'Renombrador de Archivos Configurable': 'https://github.com/Pino835/renombrador-documentos-configurable',
}


class Command(BaseCommand):
    help = 'Actualiza github_url de proyectos existentes por titulo (idempotente).'

    def handle(self, *args, **options):
        for title, url in LINKS.items():
            updated = Project.objects.filter(title=title).update(github_url=url)
            if updated:
                self.stdout.write(self.style.SUCCESS(f'{title} -> {url}'))
            else:
                self.stdout.write(self.style.WARNING(f'No se encontro proyecto con titulo "{title}"'))
