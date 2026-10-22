
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class AdminUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[
            ('staff', 'Staff'),
            ('driver', 'Driver'),
        ],
        label='Account role'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role']


class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['role'].choices = [
            ('staff', 'Staff'),
            ('driver', 'Driver'),
        ]
