from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Post
from users.models import User


class PostCreateViewTest(TestCase):
    def setUp(self):

        self.client = Client()
        self.url = reverse("blog:post_create")

        self.user = User.objects.create(
            email="email@example.com",
            password="testpassword123",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

    def test_redirect_anonymous_user(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        expected_redirect_url = reverse("users:login") + "?next=" + self.url

        self.assertRedirects(response, expected_redirect_url)


    def test_authenticated_user(self):

        # Create client
        self.client.force_login(self.user)

        # Test get response
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')

        # Test post response

        form_data = {
            "title": "Test title",
            "content": "Test content",
            "is_published": True,
        }

        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.post = Post.objects.get(title="Test title")

        self.assertTrue(self.post)

        self.assertRedirects(response, reverse('blog:post_detail', kwargs={"pk": self.post.id}))

    def test_authenticated_user_spam(self):
        """Test view wint spam title. Post wasn't saved in DB."""

        self.client.force_login(self.user)
        form_data = {
            "title": "казино",
            "content": "Test content",
            "is_published": True,
        }
        response = self.client.post(self.url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(title="казино").exists())

