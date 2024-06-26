from tkinter import Image
from django.test import TestCase
from app.forms import FeedbackForm, BlogForm, CommentForm


class FormsTestCase(TestCase):

    def test_feedback_form_valid(self):
        form_data = {
            'name': 'aboba',
            'like': 'i like your site!',
            'upgrade': 'nothing',
            'recommend': '1',
            'level': '2',
            'notice': True,
            'email': 'aboba@example.com',
            'message': 'Lorem ipsum dolor sit amet.'
        }
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_feedback_form_invalid(self):
        form_data = {
            'name': 'aboba',
            'like': 'i like your site!',
            'upgrade': 'nothing',
            'recommend': '1',
            'level': '2',
            'notice': True,
            'email': 'invalid_email',
            'message': 'Lorem ipsum dolor sit amet.'
        }
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_blog_form_valid(self):
        form_data = {
            'title': 'Test blog',
            'description': 'Short info',
            'content': 'Full blog text',
            'image': 'image1.jpg'
        }
        form = BlogForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blog_form_invalid(self):
        form_data = {
            'title': 'Test blog',
            'description': '',
            'content': 'Full blog text',
            'images': ['image1.jpg', 'image2.jpg']
        }
        form = BlogForm(data=form_data, files=form_data)
        self.assertFalse(form.is_valid())

    def test_comment_form_valid(self):
        form_data = {'text': 'This is a comment.'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        form_data = {'text': ''}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
