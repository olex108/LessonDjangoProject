import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from src.mailing import send_welcome_email

from .forms import UserRegistrationForm, UserUpdateForm
from .models import User


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = "users/user_update_form.html"
    success_url = reverse_lazy("users:user_update")

    def get_object(self, queryset=None):
        return self.request.user


class UserRegistrationView(CreateView):
    """CBV for registrate user with GET request"""

    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        """Method update to create token and send email by function send_welcome_email()"""

        user = form.save()
        user.is_active = False
        # create email verification of user
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email_confirm/{token}/"
        send_welcome_email(user.email, url)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        response = super().form_invalid(form)
        response.context_data["error_message"] = "Please correct the errors below."
        return response


def email_verification(request, token):
    """View function change param of field is_active of user if token by request is equal token in database"""

    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))
