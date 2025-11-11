from django import forms


SPAM_WORDS = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]
IMAGE_MAX_SIZE = 5 * 1024 * 1024  # MB
IMAGE_FORMATS = ["JPEG", "PNG"]


def validator_spam_words(value: str) -> None:
    """Validate spam words"""

    for word in SPAM_WORDS:
        if word in value.lower():
            raise forms.ValidationError(f"Содержит спам слово - {word}")


def validator_file_size(value: int | float) -> None:
    """Validate file size"""

    if value > IMAGE_MAX_SIZE:
        raise forms.ValidationError(f"Размер файла превышает {round(IMAGE_MAX_SIZE / 1024 / 1024, 0)} МБ")


def validator_file_format(value: str | float) -> None:
    """Validate file format"""

    if value not in IMAGE_FORMATS:
        raise forms.ValidationError(f"Неверный формат поддерживаемые форматы: {", ".join(IMAGE_FORMATS)}")
