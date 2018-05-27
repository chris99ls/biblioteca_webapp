from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    classe= forms.CharField(required=True)

    class Meta:
        model=User
        fields=(
            'username',
            'classe',
            'password1',
            'password2',
            )

    def save(self,commit=True):
        user = super(RegistrationForm,self).save(commit=False)
        user.classe= self.cleaned_data['classe']

        if commit:
            user.save()

        return user


