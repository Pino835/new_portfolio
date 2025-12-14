from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Project

class HomeView(TemplateView):
    """Vista principal del portafolio"""
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context
