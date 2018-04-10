from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts import models
from projects.models import Skill


User = get_user_model()

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


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ["email", "username", "password1", "password2"]
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = [
            'firstname',
            'lastname',
            'bio',
            'avatar',
        ]


class EditProfileForm(forms.ModelForm):
    firstname = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'First name',
            'class': ''
        })
    )

    lastname = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Last name',
            'class': ''
        })
    )

    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell us about yourself...',
            'class': ''
        })

    )

    avatar = forms.ImageField(
        label='Avatar',
        required=False,
        widget=forms.FileInput(attrs={
            'class': ''
        })
    )

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        help_text='Select one or more skill'
    )

    class Meta:
        model = models.UserProfile
        fields = ['firstname', 'lastname', 'bio', 'avatar', 'skills']
