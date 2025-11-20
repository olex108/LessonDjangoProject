from django.test import TestCase
from users.forms import UserRegistrationForm


class TestUserRegistrationForm(TestCase):
    def test_valid_registration(self):

        form_data = {
            "email": "email1@example.com",
            "password1": "pluhrdvb123",
            "password2": "pluhrdvb123",
            "country": "Russia",
            "phone": "+77777777777",
            "avatar": ""
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form_data = {
            "email": "email1example.com",
            "password1": "pluhrdvb123",
            "password2": "pluhrdvb123",
            "country": "Russia",
            "phone": "+77777777777",
            "avatar": ""
        }
        form = UserRegistrationForm(data=form_data)
        self.assertEqual(form.errors["email"], ['Enter a valid email address.'])

    def test_invalid_password(self):
        form_data = {
            "email": "email1@example.com",
            "password1": "password123",
            "password2": "password123",
            "country": "Russia",
            "phone": "+77777777777",
            "avatar": ""
        }
        form = UserRegistrationForm(data=form_data)
        self.assertEqual(form.errors["password2"], ['This password is too common.'])

    def test_invalid_phone(self):
        form_data = {
            "email": "email1@example.com",
            "password1": "pluhrdvb123",
            "password2": "pluhrdvb123",
            "country": "",
            "phone": "77777777777",
            "avatar": ""
        }
        form = UserRegistrationForm(data=form_data)
        self.assertEqual(form.errors["phone"], ['Enter a valid phone number (e.g. +12125552368).'])
