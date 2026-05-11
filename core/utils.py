import re
from io import BytesIO
from random import choice
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from core.constants import (
    AVATAR_BG_PALETTE,
    AVATAR_FILENAME,
    AVATAR_FONT,
    AVATAR_FONT_SIZE,
    AVATAR_SIZE,
    COLOR_WHITE,
    GITHUB_URL_PATTERN,
    MSG_GITHUB_INVALID,
    MSG_PHONE_INVALID,
    MSG_PHONE_TAKEN,
    PHONE_PATTERN,
)


def generate_avatar(name: str) -> ContentFile:
    bg_color = choice(AVATAR_BG_PALETTE)
    letter = name[0].upper() if name else "?"

    image = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), bg_color)
    canvas = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(AVATAR_FONT, AVATAR_FONT_SIZE)
    except IOError:
        font = ImageFont.load_default()

    bbox = canvas.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    position = (
        (AVATAR_SIZE - text_width) / 2,
        (AVATAR_SIZE - text_height) / 2,
    )
    canvas.text(position, letter, fill=COLOR_WHITE, font=font)

    buffer = BytesIO()
    image.save(buffer, format="PNG")

    filename = AVATAR_FILENAME.format(uuid=uuid4())

    return ContentFile(buffer.getvalue(), name=filename)


def clean_phone(phone, model=None, instance_pk=None):
    phone = (phone or "").strip()
    if not phone:
        return phone

    if not re.match(PHONE_PATTERN, phone):
        raise ValidationError(MSG_PHONE_INVALID)

    normalized = "+7" + phone[1:] if phone.startswith("8") else phone

    if model and _field_taken(model, "phone", normalized, instance_pk):
        raise ValidationError(MSG_PHONE_TAKEN)

    return normalized


def clean_github_url(url, model=None, instance_pk=None, error_msg=None):
    url = (url or "").strip()
    if not url:
        return url

    if not re.match(GITHUB_URL_PATTERN, url):
        raise ValidationError(MSG_GITHUB_INVALID)

    normalized = url.rstrip("/")

    if model and _field_taken(model, "github_url", normalized, instance_pk):
        raise ValidationError(error_msg)

    return normalized


def _field_taken(model, field, value, instance_pk=None):
    qs = model.objects.filter(**{field: value})
    if instance_pk:
        qs = qs.exclude(pk=instance_pk)
    return qs.exists()
