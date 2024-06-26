from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import Tickets, Blog, Comment
from app.forms import BlogForm, CommentForm
from datetime import datetime
import json


class TicketViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('ticket_view')
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_ticket_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/layout.html')

    def test_ticket_view_post_invalid_form(self):
        form_data = {
            'age': '',
            'status': '',
            'attractions': '',
            'group': '',
            'price': ''
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        

class BasketViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('basket')
        self.session = self.client.session
        self.session['ticket_data'] = [{
            'age': 'Взрослый',
            'status': 'Standard',
            'attractions': 'Шейкер',
            'group': 'Экстремальные аттракционы',
            'price': 900,
            'count': 1
        }]
        self.session.save()

    def test_basket_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/basket.html')
        self.assertEqual(response.context['total_price'], 900)
        

class ConfirmOrderViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('confirm_order')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_confirm_order_post_invalid_data(self):
        response = self.client.post(self.url, {'ticket_data': 'invalid data'}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Корзина пуста'})
        

class MyTicketsViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('my_tickets')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.ticket = Tickets.objects.create(
            user=self.user,
            age='adult',
            status='standard',
            attractions='shaker',
            price=900
        )

    def test_my_tickets_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/my_tickets.html')
        self.assertContains(response, 'Шейкер')
        

class FeedbackViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('feedback')

    def test_feedback_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/feedback.html')

    def test_feedback_view_post_valid_form(self):
        form_data = {
            'name': 'Test User',
            'like': 'yes',
            'upgrade': 'more rides',
            'recommend': '1',
            'level': '1',
            'notice': True,
            'email': 'test@example.com',
            'message': 'Great park!'
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')
        self.assertContains(response, 'Great park!')
   

class RegistationViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.blog = Blog.objects.create(
            title='Test Blog',
            content='Test Content',
            posted=datetime.now(),
            author=self.user
        )

    def test_registration_get(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/registration.html')

    def test_registration_post(self):
        data = {
            'username': 'newuser',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post(reverse('registration'), data)
        self.assertEqual(response.status_code, 302)  # Redirect to 'home'
        self.assertTrue(User.objects.filter(username='newuser').exists())


class NewpostViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_newpost_view_get(self):
        response = self.client.get(reverse('newpost'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/newpost.html')

    def test_newpost_view_post(self):
        data = {
            'title': 'New Blog',
            'content': 'Content',
            'description': 'Description',
            'image': ''
        }
        response = self.client.post(reverse('newpost'), data)
        self.assertEqual(response.status_code, 302)  # Redirect to 'blog'
        self.assertTrue(Blog.objects.filter(title='New Blog').exists())
        