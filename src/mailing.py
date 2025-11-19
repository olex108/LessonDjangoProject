from django.core.mail import send_mail
import os


def send_welcome_email(user_email: str, url: str) -> None:
    subject = "Добро пожаловать в сервис \"Каталог\""
    message = f"""Спасибо что зарегистрировались на нашем сервисе! Перейдите по ссылке для подтверждения почты {url}.
Теперь вы можете создавать и редактировать позиции по сайту"""
    from_email = os.getenv("EMAIL_ADDRESS")
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


def send_email_100_views(user_email: str, post_title: str) -> None:
    subject = "У вас новое достижение в сервисе \"Каталог\""
    message = f"Поздравляем пост \"{post_title}\" набрал первые 100 просмотров"
    from_email = os.getenv("EMAIL_ADDRESS")
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
