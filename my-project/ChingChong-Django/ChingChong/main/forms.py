from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import User

class UserEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True,)
    email = forms.EmailField(max_length=60, required=True,)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('A user with that email already exists.')
        return email
    
    class Meta:
        model = get_user_model()
        fields = ("email", 'birthday', 'number', 'food', 'aboutMe')
