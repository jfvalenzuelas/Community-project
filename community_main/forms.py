from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.utils.translation import gettext as _

class UserForm(forms.ModelForm):
    class Meta:
        model = User

        fields = (
            'first_name',
            'last_name',
            'email',
        )

        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'email': _('E-mail'),
        }

        error_messages = {
            'first_name': {
                'required': _('Please, enter your first name') 
            },
            'last_name': {
                'required': _('Please, enter your last name')
            },
            'email': {
                'required': _('Please, enter your e-mail address')
            },
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = (
            'birth_date',
        )

        widgets = {
            'birth_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'datepicker','type':'date'}),
        }

class UserProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = (
            'picture',
        )