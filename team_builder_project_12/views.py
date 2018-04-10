from django.views import generic
from django.db.models import Q

from projects.models import *


class HomeView(generic.ListView):
    model = Project
    projects = Project.objects.all()
    template_name = 'index.html'
    context_object_name = 'project'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('q')
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term) |
                Q(requirements__icontains=search_term)
            )
        return queryset


class NeedView(generic.ListView):
    model = Project
    projects = Project.objects.all()
    template_name = 'index.html'
    context_object_name = 'project'

    def get(self, request, *args, **kwargs):
        queryset = super().get_queryset()
        search_term = kwargs['need']
        self.object_list = self.filter(search_term, queryset)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('need')
        return self.filter(search_term, queryset)

    def filter(self, search_term, queryset):
        if search_term and search_term != 'All Needs':
            queryset = Project.objects.filter(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term) |
                Q(requirements__icontains=search_term) |
                Q(positions__skills__name__icontains=search_term)
            )
        return queryset
