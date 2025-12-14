from django.db import models

class Project(models.Model):
    """Modelo para almacenar proyectos del portafolio"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', null=True, blank=True)
    technologies = models.CharField(max_length=500, help_text="Tecnologías separadas por comas")
    github_url = models.URLField(blank=True, null=True)
    demo_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __str__(self):
        return self.title

    def get_technologies_list(self):
        """Retorna lista de tecnologías"""
        return [tech.strip() for tech in self.technologies.split(',')]