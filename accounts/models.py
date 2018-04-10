from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings

from projects.models import *


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            username = email.split('@')[0]

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email,
            username,
            password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return "@{}".format(self.username)

    def get_short_name(self):
        return self.username

    def get_long_name(self):
        return "@{} ({})".format(self.username, self.email)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    firstname = models.CharField(max_length=40, default='', blank=True)
    lastname = models.CharField(max_length=40, default='', blank=True)
    bio = models.TextField(blank=True, default='')
    skills = models.ManyToManyField(Skill)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse("accounts:profile", {'username': self.user.username})

    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


class UserApplication(models.Model):
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='application')
    project = models.ForeignKey(Project)
    position = models.ForeignKey(Position, related_name='applications')
    is_accepted = models.NullBooleanField(default=None)

    def __str__(self):
        return '{} -- {} for {}'.format(self.applicant, self.position, self.project)
