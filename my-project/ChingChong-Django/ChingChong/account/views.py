from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from posts.models import *
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import *
from django.contrib.auth import login, logout, get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# AUTHENTIFICATION AND REGISTRATION...

def login_user(req):
    AuthForm = AuthenticationForm()
    error = False

    if req.method == 'POST':
        AuthForm = AuthenticationForm(data=req.POST, request=req)
        if AuthForm.is_valid():
            user = AuthForm.get_user()
            login(req, user)
            return redirect('index')
        error = True
        
    return render(req, 'account/Authorization.html', {'form': AuthForm, "error": error})

def logout_user(req):
    if req.user.is_authenticated:
        logout(req)
    
    return redirect('index')

def register(req):
    RegisterForm = UserRegisterForm()
    if req.method == 'POST':
        genderM = req.POST.get('genderM')
        genderF = req.POST.get('genderF')

        RegisterForm = UserRegisterForm(data=req.POST)
        if RegisterForm.is_valid():
            user = RegisterForm.save()
            login(req, user)
            return redirect('profile')
        else:
            print( RegisterForm.errors.as_json() )
        

    return render(req, 'account/Registration.html', {'form': RegisterForm})


# PASSWORD RESTORATION STUFF...

# Страничка с формой ввода Email, для восст. пароля.
def forgot(req):
    if req.method == "GET":
        EmailForm = PasswordResetForm()
    else:
        EmailForm = PasswordResetForm(req.POST)
        if EmailForm.is_valid():
            EmailForm.save(request=req, email_template_name="emails/password_reset_email.html")
            return redirect('reset_password_confirm')

    return render(req, "account/RePassword.html", { "form": EmailForm })

def reset_confirmed(req, uidb64, token):
    id = urlsafe_base64_decode(uidb64).decode()
    user = get_user_model().objects.get(pk=id)

    if PasswordResetTokenGenerator().check_token(user, token):
        if req.method == "GET":
            PassForm = SetPasswordForm(user=user)
        else:
            PassForm = SetPasswordForm(user, data=req.POST)
            if PassForm.is_valid():
                PassForm.save()
                login(req, user)
                # print("Password has Changed")
                return redirect('profile')
            print(PassForm.errors.as_json())

        return render(req, "account/NewPassword.html", { "form": PassForm }) 
    else:
        return PermissionDenied()


# PROFILE STUFF...

def profile(req, name=None):
    # If name is none, we assume user want to see their own profile.
    if name is None:
        if req.user.is_authenticated:
            user = req.user
            
        else:
            raise PermissionDenied("You are not authenticated to view your profile")
    else:
        user = get_object_or_404(get_user_model(), username=name)
    
    amount = len( user.post_set.filter(publish=True) )
    likes = len( PostInfo.objects.filter(post__sender=user, rating=1) )

    return render(req, "account/PersonalSpace.html", {'current': user, 'postAmount': amount, 'postLikes': likes})