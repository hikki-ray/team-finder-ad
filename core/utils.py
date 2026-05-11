from io import BytesIO
from random import choice
from uuid import uuid4

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from core.constants import (
    AVATAR_BG_PALETTE,
    AVATAR_FILENAME,
    AVATAR_FONT,
    AVATAR_FONT_SIZE,
    AVATAR_SIZE,
    COLOR_WHITE,
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
