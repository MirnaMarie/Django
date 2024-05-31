"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models import Comment
from .models import Blog


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'label',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'label',
                                   'placeholder':'Пароль'}))


class FeedbackForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "label"}), label='Ваше имя', min_length=1, max_length=100)
    like = forms.CharField(label='Что вам понравилось в нашем сайте?',
                              widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'class': 'label'}))
    upgrade = forms.CharField(label='Что можно улучшить?', 
                              widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'class': 'label'}))
    recommend = forms.ChoiceField(label='Вы порекомендуете нас своим друзьям и коллегам?',
                               choices=[('1', 'Да'), ('2', 'Нет')],
                               widget=forms.RadioSelect, initial=1)
    level = forms.ChoiceField(widget=forms.Select(attrs={"class": "label"}), label='Как бы вы оценили общий уровень удовлетворенности работой нашего сайта?',
                                 choices=(('1', 'Крайне удовлетворён'),
                                          ('2', 'Удовлетворён'),
                                          ('3', 'Неудовлетворён'),
                                          ('4', 'Крайне неудовлетворён')), initial=1)
    notice = forms.BooleanField(label='Получать новости сайта на e-mail?',
                                required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "label"}), label='Ваш e-mail', min_length=7)
    message = forms.CharField(label='Что еще вы хотели бы сообщить нам, чтобы улучшить наш сайт?',
                              widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'class': 'label'}))

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        labels = {'text': "Комментарий"}
        fields = ('text',)


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image')
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content': "Полное содержание", 'image': "Картинка"}