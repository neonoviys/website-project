from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register, name='registration'),
    path('password_reset', views.forgot, name='reset_password'),
    path('password_reset/confirmed', TemplateView.as_view(template_name="account/RePasswordText.html"), name='reset_password_confirm'),
    path('password_reset/<uidb64>/<token>/', views.reset_confirmed),
    path('profile/<str:name>/', views.profile, name="check_profile"),
    path('profile/', views.profile, name="profile"),
]