from django import forms
from PIL import Image

from src.validators import validator_file_format, validator_file_size, validator_spam_words

from .models import Post


class PostForm(forms.ModelForm):
    """
    Form for post model

    !!! Add publish_status field
    """

    class Meta:
        model = Post
        exclude = ["created_at", "views_counter", "is_published", "author"]

    def __init__(self, *args, **kwargs):
        # Get and del user from form kwargs
        self.user = kwargs.pop("user", None)

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
                # "required": "required",
            }
        )
        self.fields["publish_status"].widget.attrs.update(
            {"class": "form-select form-select-lg mb-3", "aria-label": "Default select example"}
        )

        if not self.user.has_perm("blog.can_publish_post"):
            # If user don`t has permission to publish post fild "Publish" will be deleted from choises
            current_choices = list(self.fields["publish_status"].choices)
            filtered_choices = [choice for choice in current_choices if choice[0] != "PUBLISH"]
            self.fields["publish_status"].choices = filtered_choices

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
