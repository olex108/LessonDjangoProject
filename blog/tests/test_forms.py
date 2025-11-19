from django.test import TestCase
from blog.forms import PostForm

class PostFormTest(TestCase):
    def test_form_valid_post(self):

        form_data = {
            "title": "Test title",
            "content": "Test content",
            "is_published": True,
            "image": None
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_post(self):

        form_data = {
            "title": "",
            "content": "Test content",
            "is_published": True,
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["title"], ['This field is required.'])

    def test_form_spam_words(self):

        form_data = {
            "title": "казино",
            "content": "Test content",
            "is_published": True,
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["title"], ['Содержит спам слово - казино'])

