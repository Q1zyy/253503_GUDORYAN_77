from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.core.validators import RegexValidator
from .models import Client

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(
        help_text="Required. Format: DD.MM.YYYY",
        input_formats=['%d.%m.%Y']
    )
    phone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+375 \((29|33|44|25)\) \d{3}-\d{2}-\d{2}$',
                message="Phone number must be entered in the format: '+375 (29) XXX-XX-XX'. Up to 15 digits allowed."
            )
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2", "date_of_birth", "phone_number"]

    def clean_date_of_birth(self):
        den = self.cleaned_data.get('date_of_birth')
        today = date.today()
        if (den.year + 18, den.month, den.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('You must be at least 18 years old to register.')
        return den