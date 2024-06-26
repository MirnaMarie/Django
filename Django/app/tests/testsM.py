from django.test import TestCase
from app.models import Visits, Attractions, Tickets, Blog, Comment
from django.contrib.auth.models import User
from datetime import datetime

class BlogModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем пользователя
        cls.user = User.objects.create(username='testuser')
        # Создаем статью блога
        cls.blog = Blog.objects.create(
            title='Test Blog',
            description='Test Description',
            content='Test Content',
            author=cls.user
        )

    def test_blog_creation(self):
        self.assertEqual(self.blog.title, 'Test Blog')
        self.assertEqual(self.blog.description, 'Test Description')
        self.assertEqual(self.blog.content, 'Test Content')
        self.assertEqual(self.blog.author.username, 'testuser')

    def test_blog_str(self):
        self.assertEqual(str(self.blog), 'Test Blog')

    def test_blog_get_absolute_url(self):
        self.assertEqual(self.blog.get_absolute_url(), f'/blogpost/{self.blog.id}/')


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем пользователя и статью блога
        cls.user = User.objects.create(username='testuser')
        cls.blog = Blog.objects.create(
            title='Test Blog',
            description='Test Description',
            content='Test Content',
            author=cls.user
        )
        # Создаем комментарий
        cls.comment = Comment.objects.create(
            text='Test Comment',
            author=cls.user,
            post=cls.blog
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.text, 'Test Comment')
        self.assertEqual(self.comment.author.username, 'testuser')
        self.assertEqual(self.comment.post.title, 'Test Blog')

    def test_comment_str(self):
        self.assertEqual(str(self.comment), f'Комментарий {self.comment.id} {self.comment.author} к {self.comment.post}')


class TicketsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='testuser')
        cls.ticket = Tickets.objects.create(
            user=cls.user,
            age='adult',
            status='standard',
            attractions='shaker'
        )

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.user.username, 'testuser')
        self.assertEqual(self.ticket.age, 'adult')
        self.assertEqual(self.ticket.status, 'standard')
        self.assertEqual(self.ticket.attractions, 'shaker')
        self.assertEqual(self.ticket.price, 900)  # Assuming the price logic is correct

    def test_ticket_str(self):
        self.assertEqual(str(self.ticket), f'Ticket {self.ticket.id} for {self.ticket.user.username}')


class AttractionsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.attraction = Attractions.objects.create(
            name='Roller Coaster',
            thematic_group='extrim',
            price=1200
        )

    def test_attraction_creation(self):
        self.assertEqual(self.attraction.name, 'Roller Coaster')
        self.assertEqual(self.attraction.thematic_group, 'extrim')
        self.assertEqual(self.attraction.price, 1200)

    def test_attraction_str(self):
        self.assertEqual(str(self.attraction.name), 'Roller Coaster')


class VisitsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='testuser')
        cls.ticket = Tickets.objects.create(
            user=cls.user,
            age='adult',
            status='standard',
            attractions='shaker'
        )
        cls.attraction = Attractions.objects.create(
            name='Roller Coaster',
            thematic_group='extrim',
            price=1200
        )
        cls.visit = Visits.objects.create(
            ticket=cls.ticket,
            attraction=cls.attraction
        )

    def test_visit_creation(self):
        self.assertEqual(self.visit.ticket, self.ticket)
        self.assertEqual(self.visit.attraction, self.attraction)

    def test_visit_str(self):
        self.assertEqual(f"Visit {self.visit.id} to {str(self.visit.attraction.name)}", f'Visit {self.visit.id} to {self.visit.attraction.name}')

        
