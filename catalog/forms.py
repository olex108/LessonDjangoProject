from django import forms

from catalog.models import Product
from PIL import Image

from src.valodators import validator_file_format, validator_file_size, validator_spam_words


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Название продукта",
            }
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Описание продукта",
            }
        )

        self.fields["image"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "formFile",
                "required": "required",
            }
        )
        self.fields["category"].widget.attrs.update(
            {"class": "form-select", "size": "3", "aria-label": "size 3 select example"}
        )
        self.fields["price"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )
        self.fields["in_stock"].widget.attrs.update(
            {
                "class": "form-check-input",
            }
        )

    def clean_name(self):
        name = self.cleaned_data.get("name")
        validator_spam_words(name)
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        validator_spam_words(description)
        return description

    def clean_image(self):
        image_file = self.cleaned_data.get("image")
        if image_file:
            # Validation size of file
            validator_file_size(image_file.size)
            with Image.open(image_file) as image:
                # Validation format of file
                validator_file_format(image.format)
        return image_file

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if not isinstance(price, int) and not isinstance(price, float):
            raise forms.ValidationError("Цена должна быть целым или дробным числом")
        if price < 0:
            raise forms.ValidationError("Цена должна быть больше 0")
        return price
