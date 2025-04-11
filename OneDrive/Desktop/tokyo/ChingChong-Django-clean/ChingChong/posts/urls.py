from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('create', views.postCreate, name='create_post'),
    path('all', views.postAll, name="all_posts"),
    path('mine', views.postMine, name="my_posts"),
    path('edit/<int:id>', views.postEdit, name="edit_post"),
    path('delete/<int:id>', views.postDelete, name="delete_post"),
    path('api/like/<int:id>', views.postLike, name="api_post_like"),
    path('api/dislike/<int:id>', views.postDislike, name="api_post_dislike"),
    path('api/getPosts', views.apiPosts, name="api_get_posts"),
]