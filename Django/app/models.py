"""
Definition of models.
"""

from email.policy import default
from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User



# Create your models here.
class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")
    
    
    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"

admin.site.register(Blog)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(verbose_name = "Текст комментария")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата комментария")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор комментария")
    post = models. ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья комментария")
    
    def __str__(self):
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)

    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарии к статье блога"
        verbose_name_plural = "Комментарии к статьям блога"
    
admin.site.register(Comment)

class Tickets(models.Model):
    AGE = [
        ('adult', 'Взрослый'),
        ('child', 'Детский'),
        ]
    
    STATUS = [
        ('standard', 'Standard'),
        ('vip', 'VIP'),
        ('platinum', 'Platinum'),
        ]
    
    ATTRACTIONS = [
        ('Детские', (
         ('osminog', 'Осьминожка'),
         ('fire', 'Пожарная команда'),
         ('aviat', 'Авиаторы'),
         )
        ),
        ('Семейные', (
         ('koleso', 'Колесо обозрения'),
         ('katam', 'Катамараны'),
         ('gonki', 'Крутые гонки'),
         )
        ),
        ('Экстремальные', (
         ('katap', 'Катапульта'),
         ('shaker', 'Шейкер'),
         ('free', 'Свободное падение'),
         )
        ),
        ]
    
    GROUP = [
        ('extrim', 'Экстремальные аттракционы'),
        ('family', 'Семейные аттракционы'),
        ('child', 'Детские аттракционы'),
        ]
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Покупатель")
    age = models.CharField(max_length = 100, choices=AGE, default = 'adult', verbose_name = "Тип билета")
    status= models.CharField(max_length = 100, choices=STATUS, default = 'standard', verbose_name = "Статус билета")
    attractions = models.CharField(max_length = 100, choices=ATTRACTIONS, null=True, blank=True, verbose_name="Аттракционы")
    group = models.CharField(max_length = 100, choices=GROUP, null=True, blank=True, verbose_name = "Группа аттракционов")
    count = models.PositiveIntegerField(default = 1, verbose_name = "Количество")
    price = models.FloatField(default=0)
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата покупки")
    
    class Meta:
        db_table = "Tickets"
        ordering = ["-date"]
        verbose_name = "Купленные билеты"
        verbose_name_plural = "Купленные билеты"
    
    def save(self, *args, **kwargs):
        if self.status == 'platinum':
            self.attractions = None
            self.group = None
            self.price = 3000 if self.age == 'adult' else 2500
        elif self.status == 'vip':
            self.attractions = None
            if self.group == 'family':
                self.price = 1700
            elif self.group == 'extrim':
                self.price = 2200
            elif self.group == 'child':
                self.price = 1100
        elif self.status == 'standard':
            self.group = None
            attraction_prices = {
                'shaker': 900,
                'free': 950,
                'katap': 1100,
                'osminog': 450,
                'aviat': 450,
                'fire': 450,
                'koleso': 550,
                'katam': 650,
                'gonki': 750,
            }
            self.price = attraction_prices.get(self.attractions, 0)
        super().save(*args, **kwargs)

    def __str__(self): 
        return f"{self.age} - {self.status} - {self.attraction}"
    def __str__(self):
        return f"Ticket {self.id} for {self.user.username}"
    
        
        
class Attractions(models.Model):
    GROUP = (
        ('extrim', ('Экстримальные аттракционы')),
        ('family', ('Семейные аттракционы')),
        ('child', ('Детские аттракционы')),
        )
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length = 100, verbose_name = "Название аттракциона")
    thematic_group = models.CharField(max_length = 100, choices=GROUP, verbose_name = "Группа аттракционов")
    price = models.FloatField()
    
    class Meta:
        db_table = "Attractions"
        ordering = ["id"]
        verbose_name = "Аттракционы"
        verbose_name_plural = "Аттракционы"
        
class Visits(models.Model):
    id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Tickets, on_delete = models.CASCADE, verbose_name = "Билет")
    attraction = models.ForeignKey(Attractions, on_delete = models.CASCADE, verbose_name = "Аттракционы")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата посещения")
    
    class Meta:
        db_table = "Visits"
        ordering = ["-date"]
        verbose_name = "Посещения"
        verbose_name_plural = "Посещения"
        
admin.site.register(Tickets)
admin.site.register(Attractions)
admin.site.register(Visits)