from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from main.models import Restaurant
from django.shortcuts import get_object_or_404

class PostsCreationForm(forms.ModelForm):
    def clean_restaurant(self):
        restaurant = self.data.get('restaurant')
        if restaurant is None:
            return None
        
        # Проверяем, существует ли ресторан
        try:
            restaurantObject = Restaurant.objects.get(pk=restaurant)
            return restaurantObject
        except Restaurant.DoesNotExist:
            raise ValidationError('Incorrect Restaurant selected!!')

    class Meta:
        model = Post
        fields = ['sender', 'restaurant','rating', 'review']

# class PostsEditForm(forms.ModelForm):
#     def clean_restaurant(self):
#         restaurant = self.data.get('restaurant')
#         if restaurant is None:
#             return None
        
#         # Проверяем, существует ли ресторан
#         try:
#             restaurantObject = Restaurant.objects.get(pk=restaurant)
#             return restaurantObject
#         except Restaurant.DoesNotExist:
#             raise ValidationError('Incorrect Restaurant selected!!')

#     class Meta:
#         model = Post
#         fields = ['sender', 'restaurant','rating', 'review']