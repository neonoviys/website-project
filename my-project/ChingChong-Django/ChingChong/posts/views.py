from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import *
from main.models import Restaurant
from .models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage


def postAll(req):
    page = int( req.GET.get('page', 1) )
    filter = int(req.GET.get('filter', '0'))
    paginator = getPosts( filter )

    try:
        back = page - 1 if paginator.page(page).has_previous() else None
        front = page + 1 if paginator.page(page).has_next() else None

    except EmptyPage:
        back = None
        front = None

    nav = { "back": back, "front": front, "range": paginator.page_range}
    return render(req, "posts/AllPosts.html", {"page": page, "filter": filter, "nav": nav, "restaurants": Restaurant.objects.all()})

# Получаем посты оформленные шаблонизатором
def apiPosts(req):
    page = int( req.GET.get('page', 1) )
    paginator = getPosts( int(req.GET.get('filter', '0')) )

    try:
        raw_html = render(req, "posts/api_posts.html", {"posts": paginator.page(page).object_list})
    except EmptyPage:
        raw_html = render(req, "posts/api_posts.html", {"posts": None})
    
    return JsonResponse({'html': raw_html.content.decode()})


# Вспомогательный метод который возвращает посты(QuerySet) + пагинация
def getPosts(filter):
    # Если установлен фильтр, то фильтруем посты по городу.
    if (filter != 0):
        posts = Post.objects.filter(publish=True, restaurant__pk=filter).order_by('-pk')
    else:
        posts = Post.objects.filter(publish=True).order_by('-pk')

    return Paginator(posts, 4, allow_empty_first_page=False)
    

@login_required
def postCreate(req):
    new_Post = PostsCreationForm()
    if req.method == 'POST':
        data = req.POST.copy()

        data['sender'] = req.user
        if data['restaurant'] == '0':
            data['restaurant'] = None
        
        new_Post = PostsCreationForm(data)
        if new_Post.is_valid():
            new_Post.save()
            # PostsCreationForm.add_error(new_Post, None, "Your post has been sent for moderation")
            return redirect("my_posts");

    return render(req, "posts/Book.html", {"form": new_Post, "cities": Restaurant.objects.all()})

@login_required
def postLike(req, id):
    post = get_object_or_404(Post, pk=id)

    if PostInfo.objects.filter(post=post, user=req.user).exists():
        info = PostInfo.objects.get(post=post, user=req.user)
        if info.rating == 1:
            info.delete()
        else:
            info.rating = 1
            info.save()
    else:
        info = PostInfo(post=post, user=req.user, rating=1)
        info.save()


    return redirect("all_posts")


@login_required
def postDislike(req, id):
    post = get_object_or_404(Post, pk=id)

    if PostInfo.objects.filter(post=post, user=req.user).exists():
        info = PostInfo.objects.get(post=post, user=req.user)
        if info.rating == -1:
            info.delete()
        else:
            info.rating = -1
            info.save()
    else:
        info = PostInfo(post=post, user=req.user, rating=-1)
        info.save()


    return redirect("all_posts")

@login_required
def postMine(req):
    posts = Post.objects.filter(sender=req.user).order_by('-pk')
    return render(req, "posts/MyPosts.html", {"posts": posts})


@login_required
def postEdit(req, id):
    post = get_object_or_404(Post, pk=id)
    postEditForm = PostsCreationForm(instance=post) # Can be used to edit Post too


    if (req.user == post.sender and not post.publish) or (req.user.has_perm('posts.change_post')):
        if req.method == 'POST':
            data = req.POST.copy()

            data['sender'] = req.user
            if data['restaurant'] == '0':
                data['restaurant'] = None
            
            postEditForm = PostsCreationForm(data=data, instance=post)
            if postEditForm.is_valid():
                postEditForm.save()
                # PostsCreationForm.add_error(new_Post, None, "Your post has been edited")
                return redirect("my_posts")

        return render(req, "posts/EditBook.html", {"form": postEditForm, "cities": Restaurant.objects.all()})
    
    else:
        raise PermissionDenied("You cant edit other's posts")
    
def postDelete(req, id):
    post = get_object_or_404(Post, pk=id)
    if (req.user == post.sender and not post.publish) or (req.user.has_perm('posts.delete_post')):
        post.delete()
        return redirect("my_posts")