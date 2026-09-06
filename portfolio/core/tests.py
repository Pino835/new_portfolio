from django.test import TestCase
from django.urls import reverse

from .models import Project


class HomeViewTests(TestCase):
    def test_home_page_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_index_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'index.html')

    def test_home_page_lists_projects_in_order(self):
        second = Project.objects.create(title='Segundo', description='d', technologies='Python', order=2)
        first = Project.objects.create(title='Primero', description='d', technologies='Python', order=1)

        response = self.client.get(reverse('home'))

        self.assertEqual(list(response.context['projects']), [first, second])


class ProjectModelTests(TestCase):
    def test_get_technologies_list_splits_and_strips(self):
        project = Project.objects.create(
            title='Proyecto',
            description='d',
            technologies=' Python, Django ,PostgreSQL',
        )

        self.assertEqual(project.get_technologies_list(), ['Python', 'Django', 'PostgreSQL'])

    def test_str_returns_title(self):
        project = Project.objects.create(title='Mi Proyecto', description='d', technologies='Python')

        self.assertEqual(str(project), 'Mi Proyecto')
