"""
Definition of views.
"""

from datetime import datetime
from telnetlib import STATUS
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from app.forms import FeedbackForm
from django.contrib.auth.forms import UserCreationForm

from django.db import connection, models
from .models import Attractions, Blog

from .models import Comment
from .forms import BlogForm, CommentForm

from .models import Tickets
from .forms import TicketsForm

import uuid  # импортируем модуль uuid для генерации уникальных идентификаторов
import json

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Домашняя страница',
            'year': datetime.now().year,
        }
    )

def ticket_view(request):
    age = {'adult': 'Взрослый', 'child': 'Детский'}
    status = {'standard': 'Standard', 'vip': 'VIP', 'platinum': 'Platinum'}
    attractions = {
        'osminog': 'Осьминожка', 'fire': 'Пожарная команда', 'aviat': 'Авиаторы',
        'koleso': 'Колесо обозрения', 'katam': 'Катамараны', 'gonki': 'Крутые гонки',
        'katap': 'Катапульта', 'shaker': 'Шейкер', 'free': 'Свободное падение'
    }
    group = {'extrim': 'Экстремальные аттракционы', 'family': 'Семейные аттракционы', 'child': 'Детские аттракционы'}

    ticket_data = None
    
    if request.method == 'POST':
        form = TicketsForm(request.POST)
        if form.is_valid():
            ticket_data = form.cleaned_data
            ticket_data = {
                'age': age.get(request.GET.get('age', ''), ''),
                'status': status.get(request.GET.get('status', ''), ''),
                'attractions': attractions.get(request.GET.get('attractions', ''), ''),
                'group': group.get(request.GET.get('group', ''), ''),
            }
            ticket_data['count'] = 1  # Пример добавления поля 'count'
            ticket_data['price'] = float(ticket_data['price'])
            tickets = request.session.get('ticket_data', {})
            request.session['ticket_data'] = tickets
            return redirect('basket')
        else:
            print("Форма не валидна")
            print(form.errors)
    else:
        form = TicketsForm()

    context = {
        'ticket_data': ticket_data,
        'form': form,
        'age': age,
        'status': status,
        'attractions': attractions,
        'group': group,
    }

    return render(request, 'app/layout.html', context)

def basket(request):
    tickets = request.session.get('ticket_data', {})
    total_price = 0

    for ticket in tickets:
        price = ticket.get('price')
        count = ticket.get('count', 1)
        if price:
            total_price += price * count

    context = {
        'title': 'Корзина',
        'year': datetime.now().year,
        'total_price': total_price,
        'ticket_data': tickets,
    }

    return render(request, 'app/basket.html', context)

def confirm_order(request):
    if request.method == 'POST':
        ticket_data_str = request.POST.get('ticket_data', None)

        if not ticket_data_str:
            return JsonResponse({'error': 'Корзина пуста'}, status=400)

        try:
            ticket_data = json.loads(ticket_data_str)
            if not isinstance(ticket_data, list):
                raise json.JSONDecodeError("Invalid JSON format", ticket_data_str, 0)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Неверный формат JSON'}, status=400)

        if not ticket_data:
            return JsonResponse({'error': 'Корзина пуста'}, status=400)

        for ticket in ticket_data:
            form = TicketsForm(ticket)
            if form.is_valid():
                ticket_obj = form.save(commit=False)
                ticket_obj.user = request.user if request.user.is_authenticated else None
                ticket_obj.save()
            else:
                errors = form.errors.as_json()
                return JsonResponse({'errors': errors}, status=400)
            
        return redirect('my_tickets')
        return JsonResponse({'message': 'Заказ успешно оформлен и сохранен в базе данных.'}, status=201)
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST.'}, status=405)

def update_ticket_count(request, ticket_id):
    tickets = request.session.get('ticket_data', {})

    if ticket_id in tickets:
        if 'increase' in request.POST:
            tickets[ticket_id]['count'] = tickets[ticket_id].get('count', 1) + 1
        elif 'decrease' in request.POST and tickets[ticket_id].get('count', 1) > 1:
            tickets[ticket_id]['count'] = tickets[ticket_id].get('count', 1) - 1

        request.session['ticket_data'] = tickets

    return redirect('basket')

def my_tickets(request):
    """Renders the my_tickets page with the user's tickets."""
    assert isinstance(request, HttpRequest)
    user = request.user

    # Запрашиваем билеты текущего пользователя из базы данных
    tickets = Tickets.objects.filter(user=user).order_by('-id')

    age_map = dict(Tickets.AGE)
    status_map = dict(Tickets.STATUS)
    #attractions_map = dict(Tickets.ATTRACTIONS)
    attractions = {
        'osminog': 'Осьминожка', 'fire': 'Пожарная команда', 'aviat': 'Авиаторы',
        'koleso': 'Колесо обозрения', 'katam': 'Катамараны', 'gonki': 'Крутые гонки',
        'katap': 'Катапульта', 'shaker': 'Шейкер', 'free': 'Свободное падение'
    }
    group_map = dict(Tickets.GROUP)    

    ticket_data = []
    for ticket in tickets:
        ticket_data.append({
            'id': ticket.id,
            'user': ticket.user.username,
            'age': age_map.get(ticket.age),
            'status': status_map.get(ticket.status),
            'attractions': attractions.get(ticket.attractions),
            'group': group_map.get(ticket.group),
        })
        print(ticket.attractions)
    
    
    # Передаем билеты в контекст для отображения в шаблоне
    context = {
        'tickets': ticket_data
    }

    return render(request, 'app/my_tickets.html', context)

def all_tickets_view(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    tickets = Tickets.objects.all()  # Выборка данных из базы данных
    context = {'tickets': tickets}
    return render(request, 'app/all_tickets.html', context)

def all_tickets(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/all_tickets.html',
        {
            'title':'Билеты',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Твоя контактная страница.',
            'year':datetime.now().year,
        }
    )

def feedback(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    data = None
    recommend = {'1': 'Да', '2': 'Нет'}
    level = {'1': 'Крайне удовлетворён', '2': 'Удовлетворён', 
                '3': 'Неудовлетворён', '4': 'Крайне неудовлетворён'}
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['like'] = form.cleaned_data['like']
            data['upgrade'] = form.cleaned_data['upgrade']
            data['recommend'] = recommend[ form.cleaned_data['recommend'] ]
            data['level'] = level[ form.cleaned_data['level'] ]
            if (form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = FeedbackForm()
    return render(
        request,
        'app/feedback.html',
        {
            'form':form,
            'data':data
        }
    )

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        regform = UserCreationForm (request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.save()
        return redirect('home')
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    return render(

        request,
        'app/registration.html',
        {
            'regform': regform, # передача формы в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.raw("SELECT * FROM Posts") #SQL
    #posts = Blog.objects.all() # ORM
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts, # передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    #post_1 = Blog.objects.get(id=parametr) # ORM
    post_1 = Blog.objects.raw("SELECT * FROM Posts WHERE id = %s", [parametr]) #SQL
    comments = Comment.objects.filter(post=parametr)
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
        return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm() # создание формы для ввода комментария
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
            'year':datetime.now().year,
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
        }
    )

def newpost(request):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            #blog_f = blogform.save(commit=False)
            #blog_f.author = request.user
            #blog_f.posted = datetime.now() 
            #blog_f.save() # сохраняем изменения после добавления полей
            
             #newblog=Blog.objects.create(                    #ORM
                 #=blogform.cleaned_data['title'],
                 #content=blogform.cleaned_data['content'],
                 #image=blogform.cleaned_data['image'],
                 #posted=datetime.now(),
                 #author=request.user,)
            
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Posts (title, description, content, image, posted, author_id) VALUES (%s, %s, %s, %s, %s, %s)", 
                [blogform.cleaned_data['title'], blogform.cleaned_data['description'], blogform.cleaned_data['content'], blogform.cleaned_data['image'], 
                datetime.now(), request.user.id])
                newblog=Blog.objects.get(title=blogform.cleaned_data['title'])
                return redirect('blog')
            
        return redirect('blog') # переадресация на ту же страницу статьи после отправки комментария
    else:
        blogform = BlogForm() # создание формы для ввода комментария
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform, # передача формы добавления комментария в шаблон веб-страницы
            'title': 'Добавить статью блога',
            
            'year':datetime.now().year,
        }
    )

def edit_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
             form.save()  # Сохранение данных формы в базе данных
             return redirect('blogpost', parametr=post_id)  # Перенаправление на страницу поста после редактирования

            #title = form.cleaned_data['title']
            #content = form.cleaned_data['content']
            
            # Получаем имя файла, если есть
            #if 'image' in form.cleaned_data and form.cleaned_data['image']:
                #image = form.cleaned_data['image'].name
            #else:
                #image = post.image.name  # или post.image, в зависимости от структуры модели
            

            # Обовление данных с использованием SQL-запроса
            # with connection.cursor() as cursor:
                # cursor.execute(""" UPDATE Posts SET title = %s, content = %s, image = %s WHERE id = %s """, [title, content, image, post_id])

            #return redirect('blogpost', parametr=post_id)  # Перенаправление на страницу поста после редактирования

    else:
        form = BlogForm(instance=post)
    
    return render(request, 'app/edit_post.html', {
        'form': form,
        'post': post
    })

def delete_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id, author=request.user)
    if request.method == "POST":
       post.delete()   # Удаление поста с использованием ORM
       
       # Выполнение SQL запроса для удаления данных
       # with connection.cursor() as cursor:
            # cursor.execute("DELETE FROM Posts WHERE id = %s", [post_id])
    return redirect('blog')


def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'message':'Общие сведения о нашем проекте',
            'year':datetime.now().year,
        }
    )

def child(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/child.html',
        {
            'title':'Детские аттракционы',
            'year':datetime.now().year,
        }
    )

def family(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/family.html',
        {
            'title':'Семейные аттракционы',
            'year':datetime.now().year,
        }
    )

def extrim(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/extrim.html',
        {
            'title':'Экстремальные аттракционы',
            'year':datetime.now().year,
        }
    )

def shaker(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/shaker.html',
        {
            'title':'Шейкер',
            'year':datetime.now().year,
        }
    )

def katap(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/katap.html',
        {
            'title':'Катапульта',
            'year':datetime.now().year,
        }
    )

def free(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/free.html',
        {
            'title':'Свободное падение',
            'year':datetime.now().year,
        }
    )

def osminog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/osminog.html',
        {
            'title':'Осьминожка',
            'year':datetime.now().year,
        }
    )

def fire(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/fire.html',
        {
            'title':'Пожарная команда',
            'year':datetime.now().year,
        }
    )

def aviat(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/aviat.html',
        {
            'title':'Авиаторы',
            'year':datetime.now().year,
        }
    )

def katam(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/katam.html',
        {
            'title':'Катамараны',
            'year':datetime.now().year,
        }
    )

def gonki(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/gonki.html',
        {
            'title':'Крутые гонки',
            'year':datetime.now().year,
        }
    )

def koleso(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/koleso.html',
        {
            'title':'Колесо обозрения',
            'year':datetime.now().year,
        }
    )
