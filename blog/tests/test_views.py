from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Post


class PostViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse("blog:post_create")

    def test_form_valid(self):
        form_data = {
            "title": "Test title",
            "content": "Test content",
            "is_published": True,
            "image": ""
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title="Test title").exists())

