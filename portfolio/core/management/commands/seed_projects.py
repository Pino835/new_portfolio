import json
from pathlib import Path

from django.core.management.base import BaseCommand

from core.models import Project

FIXTURE_PATH = Path(__file__).resolve().parent.parent.parent / 'fixtures' / 'initial_projects.json'


class Command(BaseCommand):
    help = 'Carga los proyectos iniciales del portafolio si la tabla esta vacia.'

    def handle(self, *args, **options):
        if Project.objects.exists():
            self.stdout.write('Ya hay proyectos en la base de datos, no se carga nada.')
            return

        with open(FIXTURE_PATH, encoding='utf-8') as f:
            data = json.load(f)

        for entry in data:
            Project.objects.create(
                title=entry['title'],
                description=entry['description'],
                technologies=entry['technologies'],
                github_url=entry['github_url'] or None,
                demo_url=entry['demo_url'] or None,
                order=entry['order'],
                image=entry['image'] or None,
            )

        self.stdout.write(self.style.SUCCESS(f'{len(data)} proyectos cargados correctamente.'))
