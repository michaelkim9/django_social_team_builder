from django.conf import settings
from django.db import models

from django.core.urlresolvers import reverse


class Skill(models.Model):
    """User skills class."""
    ANDROID = 1
    DESIGNER = 2
    JAVA = 3
    PHP = 4
    PYTHON = 5
    RAILS = 6
    WORDPRESS = 7
    IOS = 8

    SKILL_CHOICES = (
        (str(ANDROID), 'Android Developer'),
        (str(DESIGNER), 'Designer'),
        (str(JAVA), 'Java Developer'),
        (str(PHP), 'PHP Developer'),
        (str(PYTHON), 'Python Developer'),
        (str(RAILS), 'Rails Developer'),
        (str(WORDPRESS), 'Wordpress Developer'),
        (str(IOS), 'iOS Developer')
    )

    name = models.CharField(max_length=140, choices=SKILL_CHOICES, default='unknown')

    def __str__(self):
        return self.get_name_display()


class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(default='')
    timeline = models.CharField(max_length=255, blank=True)
    complete = models.BooleanField(default=False)

    @property
    def open_positions(self):
        return self.positions.exclude(filled=True)

    def __str__(self):
        return self.title.title()

    def get_absolute_url(self):
        return reverse("projects:project_detail", kwargs={"pk": self.pk})


class Position(models.Model):
    project = models.ForeignKey(Project, default='', related_name='positions')
    name = models.CharField(max_length=140)
    description = models.TextField()
    skills = models.ManyToManyField(Skill, default='')
    filled = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.project.title.title(), self.name.title())
