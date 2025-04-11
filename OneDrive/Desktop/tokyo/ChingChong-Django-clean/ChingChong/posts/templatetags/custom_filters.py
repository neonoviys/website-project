from django import template
from django.db.models import Count

register = template.Library()

@register.filter
def count_rating(queryset, rating):
    if queryset:
        return len( queryset.filter(rating=rating) )
    return 0

@register.filter
def has_liked(queryset, user):
    if queryset:
        liked = queryset.filter(rating=1, user=user).exists()
        if liked:
            return "True"
        else:
            return "False"
    return "False"

@register.filter
def has_disliked(queryset, user):
    if queryset:
        disliked = queryset.filter(rating=-1, user=user).exists()
        if disliked:
            return "True"
        else:
            return "False"
    return "False"
