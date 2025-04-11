from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from account.models import User
from posts.models import *
from account.forms import *
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def sub(req):
    if req.method == "GET":
        return render(req, "main/Subscription.html")
    
    if req.method == "POST":
        user = User.objects.get(pk=req.user.pk)
        if req.user.number == "":
            user.number = req.POST.get("number", "")
        
        user.subscribed = not user.subscribed
        user.save()
        return JsonResponse({"success": True})

@csrf_exempt
def search_city(req):
    query = req.GET.get('city', None)
    if query:
        query = req.GET.get('city', '')
        # Выполнение поиска по базе city__icontains
        results = Cities.objects.filter(city__icontains=query).values('city')[:5]
        return JsonResponse({'results': list(results)})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def unique_name(req):
    query = req.GET.get('name', None)
    if query:
        results = User.objects.filter(username=query).exists()
        return JsonResponse({'results': not results})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def unique_email(req):
    query = req.GET.get('email', None)
    if query:
        results = User.objects.filter(email=query).exists()
        return JsonResponse({'results': not results})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

# Я бы лучше переделал бы это с формой, но у меня нет времени!!!
def profile_update(req):
    if req.method == "POST":
        user = req.user  # Текущий пользователь

        # Обновление текстовых полей (если не пустые)
        if req.POST.get("number"):
            user.number = req.POST["number"]
        if req.POST.get("city"):
            city = Cities.objects.get(city=req.POST["city"])
            user.city = city
        if req.POST.get("aboutMe"):
            user.aboutMe = req.POST["aboutMe"]
        if req.POST.get("food"):
            user.food = req.POST["food"]
        if req.POST.get("birthday"):
            user.birthday = datetime.strptime(req.POST["birthday"], "%Y-%m-%d").date()

        # Обновление аватара
        if "avatar" in req.FILES:
            user.profilePic = req.FILES["avatar"]

        user.save()  # Сохранение изменений
        return redirect('profile')