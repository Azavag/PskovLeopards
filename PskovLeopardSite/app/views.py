"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime
from .forms import PoolForm
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog
from .models import Comment
from .forms import CommentForm
from .forms import BlogForm
from django.views.generic import DetailView

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя страница',
            'year':datetime.now().year,
        }
    )

def tickets(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/tickets.html',
        {
            'title':'Билеты',
            'message':'Страница покупки билетов.',
            'year':datetime.now().year,
        }
    )

def timetable(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/timetable.html',
        {
            'title':'Расписание',
            'message':'Описание вашего приложения здесь.',
            'year':datetime.now().year,
        }
    )
def links(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Ссылки',
            'year':datetime.now().year,
        }
    )
def roster(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/roster.html',
        {
            'title':'Состав',
            'message':'',
            'year':datetime.now().year,
        }
    )

def stats(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/stats.html',
        {
            'title':'Статистика',
            'message':'',
            'year':datetime.now().year,
        }
    )
def shop(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/shop.html',
        {
            'title':'Магазин',
            'message':'',
            'year':datetime.now().year,
        }
    )
def pool(request):

    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    internet = {'1': 'Каждый день', '2': 'Несколько раз в день', '3': 'Несколько раз в неделю', '4': 'Несколько раз в месяц'}
    if request.method == 'POST':
        form = PoolForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['job'] = form.cleaned_data['job']
            data['gender'] = gender[ form.cleaned_data['gender']]
            data['internet'] = internet[form.cleaned_data['internet']]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = PoolForm()
    return render(
        request,
        'app/pool.html',
        {
            'title':'Отзыв',
            'form':form,
            'data':data,
            'message':'',
            'year':datetime.now().year,
        }
    )

def registration(request):
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            regform.save()

            return redirect('home')
    else:           
        regform = UserCreationForm()       
    return render(
    request, 'app/registration.html',
    {
        'regform': regform,
        'year':datetime.now().year,
        }
    )

def blog(request):
    posts = Blog.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title':'Новости хоккея',
            'posts': posts,
            'year': datetime.now().year,
        }
    )


def blogpost(request, parametr):
     assert isinstance(request, HttpRequest)
     post_1 = Blog.objects.get(id=parametr)
     comments = Comment.objects.filter(post = parametr)

     if request.method == "POST":
         form = CommentForm(request.POST)
         if form.is_valid():
             comment_f = form.save(commit = False)
             comment_f.author = request.user
             comment_f.date = datetime.now()
             comment_f.post = Blog.objects.get(id=parametr)
             comment_f.save()

             return redirect('blogpost', parametr = post_1.id)
     else:
        form = CommentForm()

     return render(
        request,
        'app/blogpost.html',
        {
            'post_1':post_1,
            'year':datetime.now().year,
        }
    )
def newpost(request):
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()           
            blog_f.author = request.user 
            blog_f.save() 
            return redirect('blog') 
    else:
        blogform = BlogForm() 
    
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить новость',
            'year': datetime.now().year,
        }
    )

def videopost(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Интересные видео',
            'year':datetime.now().year,
        }
    )
 