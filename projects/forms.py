from django import forms

from . import models


class ProjectCreateForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Project Title',
                'class': 'circle--input--h1'
            })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Project description...'})
    )

    requirements = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': ''})
    )

    timeline = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Time estimate',
                'class': 'circle--textarea--input'
            })
    )

    class Meta:
        model = models.Project
        fields = ('title', 'description', 'timeline', 'requirements')


class PositionCreateForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Position Title',
                'class': ''
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Position description...',
                'class': ''
            }
        )
    )

    skills = forms.ModelMultipleChoiceField(
        queryset=models.Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        help_text='Select one or more skill'
    )

    class Meta:
        model = models.Position
        fields = ('name', 'description', 'skills')


PositionFormSet = forms.modelform_factory(
    models.Position,
    form=PositionCreateForm
)

PositionInlineFormSet = forms.modelformset_factory(
    models.Position,
    form=PositionCreateForm,
    fields=('name', 'description', 'skills'),
    extra=5,
)
