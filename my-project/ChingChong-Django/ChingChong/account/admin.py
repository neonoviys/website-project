from django.contrib import admin
from . models import *
from django.templatetags.static import static
from django.contrib.auth.admin import UserAdmin


# Пока хотя бы так
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'gender', 'date_joined', 'is_active', 'is_staff')
    fieldsets = list(UserAdmin.fieldsets)
    # Видоизменяем стандартные fieldsets
    fieldsets[0] = (
        None,
        {
            'fields': ('username', 'password', 'email'),  # Перемещаем email сюда
        },
    )
    fieldsets[1] = (
        'Personal Info',
        {
            'fields': ('gender', 'number', 'city', 'food', 'birthday', 'aboutMe', 'profilePic'),  # Перевернули тут все вверх-дном!!
        },
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ("is_superuser", "last_login", "date_joined")  # НЕ Суперпользователям - нельзя стать суперпользователями.
        return super().get_readonly_fields(request, obj)
    
    def has_change_permission(self, request, obj=None):
        if obj: 
            if (obj.is_superuser and not request.user.is_superuser):
                return False  # Суперадмина нельзя менять никому(искл: суперадмины)
            
            # is_obj_moderator = obj.groups.filter(name="Moderators").exists()
            # if (is_obj_moderator and not request.user.is_superuser) and obj != request.user:
            #     return False  # Модераторы не могут менять Модераторов (искл: суперадмины, и сам себя)
        
        return super().has_change_permission(request, obj)


