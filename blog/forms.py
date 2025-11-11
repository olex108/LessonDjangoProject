from django import forms

from .models import Post
from PIL import Image

from src.valodators import validator_file_format, validator_file_size, validator_spam_words


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["created_at", "views_counter"]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Заголовок поста",
            }
        )
        self.fields["content"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Текст поста",
            }
        )

        self.fields["image"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "formFile",
                "required": "required",
            }
        )
        self.fields["is_published"].widget.attrs.update(
            {
                "class": "form-check-input",
            }
        )

    def clean_title(self):
        title = self.cleaned_data.get("title")
        validator_spam_words(title)
        return title

    def clean_image(self):
        image_file = self.cleaned_data.get("image")
        if image_file:
            # Validation size of file
            validator_file_size(image_file.size)
            with Image.open(image_file) as image:
                # Validation format of file
                validator_file_format(image.format)
        return image_file
