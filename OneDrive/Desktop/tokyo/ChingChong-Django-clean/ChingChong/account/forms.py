from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from main.models import Cities

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=60, required=True,)
    # birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}, format="DD.MM.YYYY"))
    birthday = forms.DateField( widget=forms.DateInput(format="DD.MM.YYYY"), required=False )
    number = forms.CharField(max_length=11, required=False)
    city = forms.CharField(max_length=50)
    food = forms.CharField(max_length=50, required=False)
    gender = forms.CharField(max_length=10, initial='D', required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email
    
    def clean_city(self):
        city = self.cleaned_data.get('city')
        cityObject = Cities.objects.filter(city=city)
        if cityObject:
            return cityObject[0]
        
        raise ValidationError('Пожалуйста используйте корректное место проживания')
        

    def save(self, commit = ...):
        new_user = super().save(commit)
        return new_user

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "number", "gender", "birthday", "food", "city",)

# class UserEditForm(forms.ModelForm):
#     username = forms.CharField(max_length=150, required=True,)
#     email = forms.EmailField(max_length=60, required=True,)
    
#     def clean_username(self):
#         name = self.cleaned_data.get('username')
#         if User.objects.filter(username=name).exclude(pk=self.instance.pk).exists():
#             raise ValidationError('A user with that name already exists.')
#         return name
    
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
#             raise ValidationError('A user with that email already exists.')
#         return email
    
#     class Meta:
#         model = User
#         fields = ("username", "email",)
