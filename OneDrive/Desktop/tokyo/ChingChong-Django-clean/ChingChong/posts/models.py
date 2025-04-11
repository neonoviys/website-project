from django.db import models
from account.models import User
from main.models import Restaurant

# Create your models here.
class Post(models.Model):
    RATINGTYPE = [ (1, "1 Звезда"), (2,"2 Звезды"), (3, "3 Звезды"), (4, "4 Звезды"), (5, "5 Звезд") ]
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Отправитель")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Ресторан")
    rating = models.IntegerField("Рейтинг", choices=RATINGTYPE, default='5', blank=False)
    review = models.TextField("Отзыв", blank=False, max_length=1024)
    # likes = models.IntegerField("Лайки", default=0)
    # dislikes = models.IntegerField("Дизлайки", default=0)

    publish = models.BooleanField("Опубликован", default=False)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.publish and not self.sender:
            self.delete()
    

class PostInfo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    RATINGTYPE = [ (0, "None"), (1,"Like"), (-1, "Dislike"), ]
    rating = models.IntegerField("Оценка", choices=RATINGTYPE, default=0, blank=False)

    class Meta:
        unique_together = ("user", "post")

    # @classmethod
    # def set_user_rating(cls, post, user, rating):
    #     obj, created = cls.objects.get_or_create(post=post, user=user)
    #     if not created:
    #         obj.rating = rating
    #         obj.save()
    #     else:
    #         obj.rating = rating
    #         obj.save()
        
    #     # Обновляем количество лайков/дизлайков у поста
    #     if rating == 1:
    #         post.likes += 1
    #     elif rating == -1:
    #         post.dislikes += 1
    #     post.save()