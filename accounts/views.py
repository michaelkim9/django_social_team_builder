from braces.views import PrefetchRelatedMixin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy

from django.db.models import Q
from django.shortcuts import (get_object_or_404, reverse,
                              HttpResponseRedirect)
from django.views import generic
from django.views.generic.edit import UpdateView
from notifications.signals import notify

from . import forms
from accounts import models
from projects import models as proj

STATUS_CHOICES = {
    'new': None,
    'accepted': True,
    'rejected': False
}

User = get_user_model()


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")
    template_name = "accounts/signin.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(generic.RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/profile.html'
    login_url = settings.LOGIN_REDIRECT_URL

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        lookup = kwargs.get('username')
        user = models.User.objects.get(username=lookup)
        profile = models.UserProfile.objects.prefetch_related('skills').get(user=user)
        context['profile'] = profile
        context['skills'] = [skill for skill in profile.skills.all()]

        positions = proj.Position.objects.all()
        context['positions'] = positions.filter(Q(project__owner=user) & Q(project__complete=True))

        projects = proj.Project.objects.all()
        context['current_projects'] = projects.filter(Q(owner=user) & Q(complete=False))
        context['past_projects'] = projects.filter(Q(owner=user) & Q(complete=True))
        return context


class EditProfileView(LoginRequiredMixin, generic.UpdateView):
    model = models.UserProfile
    form = forms.EditProfileForm()
    template_name = 'accounts/profile_edit.html'

    success_url = reverse_lazy('home')
    fields = ['firstname', 'lastname', 'bio', 'avatar', 'skills']
    slug_field = 'user__username'
    slug_url_kwarg = 'username'


class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


class UserApplications(LoginRequiredMixin,
                       PrefetchRelatedMixin, generic.ListView):
    model = models.UserApplication
    template_name = 'accounts/applications.html'
    prefetch_related = ['project', 'position']

    def get_queryset(self):
        queryset = super().get_queryset()
        status_term = self.request.GET.get('status') or 'all'

        if status_term and status_term != 'all':
            if status_term in STATUS_CHOICES.keys():
                queryset = queryset.filter(
                    is_accepted=STATUS_CHOICES[status_term]
                )

    def get_context_data(self, **kwargs):
        context = super(UserApplications, self).get_context_data(**kwargs)
        applications = models.UserApplication.objects.all()
        context['applications'] = applications.filter(~Q(applicant=self.request.user))
        return context


class UserApplicationStatus(LoginRequiredMixin, generic.TemplateView):

    def get(self, request, *args, **kwargs):
        position_id = self.kwargs.get('position')
        position = proj.Position.objects.filter(pk=position_id).first()
        if position.project.owner == self.request.user:
            applicant_pk = self.kwargs.get('applicant')
            applicant = get_object_or_404(User, pk=applicant_pk)
            status = self.kwargs.get('status')
            if status == 'approve' or status == 'deny':
                if position and applicant:
                    bstatus = True if status == 'approve' else False
                    application = models.UserApplication.objects.filter(
                        position=position, applicant=applicant
                    ).update(is_accepted=bstatus)

                    if status == 'approve':
                        msg_status = 'approved'
                    else:
                        msg_status = 'denied'

                    notify.send(
                        applicant,
                        recipient=applicant,
                        verb='Your application for {} as {} was {}'.format(
                            position.project.title, position.name, msg_status
                        ),
                        description=''
                    )
                    return HttpResponseRedirect(reverse('accounts:my_applications'))
        return HttpResponseRedirect(reverse('accounts:my_applications'))


class UserNotifications(LoginRequiredMixin, PrefetchRelatedMixin, generic.TemplateView):
    template_name = 'accounts/notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unreads'] = self.request.user.notifications.unread()
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
