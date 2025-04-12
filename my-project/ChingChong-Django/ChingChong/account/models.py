from django.db import models
from django.contrib.auth.models import AbstractUser
from main.models import Cities
from django.core.exceptions import ValidationError
from datetime import date
from PIL import Image

# Create your models here.
def validate_birth_date(value):
    if value < date(1900, 1, 1):
        raise ValidationError("Дата рождения не может быть раньше 1900 года.")
    if value > date.today():
        raise ValidationError("Дата рождения не может быть в будущем.")
    
class User(AbstractUser):
    email = models.CharField("Email", max_length=50, blank=True, default='default@default.com')
    GENDERTYPE = [ ("M", "Мужской"), ("F","Женский"), ("D", "...") ]
    gender = models.CharField("Пол", max_length=10, blank=True, choices=GENDERTYPE, default='D')
    number = models.CharField("Номер Телефона", default='', max_length=16, blank=True)
    birthday = models.DateField("День Рождения", null=True, blank=True, validators=[validate_birth_date],)
    city = models.ForeignKey(Cities, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Город Проживания")
    food = models.CharField("Любимая Еда", max_length=50, blank=True)
    aboutMe = models.TextField("О Пользователе", max_length=256, blank=True, null=True)
    subscribed = models.BooleanField("Подписан", default=False)
    profilePic = models.ImageField("Аватар Пользователя", null=True, blank=True, upload_to="avatar/", default="avatar/default.png")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Сначала сохраняем изображение
        
        img_path = self.profilePic.path
        img = Image.open(img_path)

        # Обрезаем до квадратного формата (1:1)
        min_size = min(img.size)  # Берем меньшую сторону
        left = (img.width - min_size) / 2
        top = (img.height - min_size) / 2
        right = (img.width + min_size) / 2
        bottom = (img.height + min_size) / 2

        img = img.crop((left, top, right, bottom))
        img.save(img_path)  # Перезаписываем файл
