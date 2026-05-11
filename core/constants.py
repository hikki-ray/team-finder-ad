PAGE_SIZE = 9

AVATAR_SIZE = 200
AVATAR_FONT_SIZE = 100
AVATAR_FONT = "arial.ttf"
AVATAR_FILENAME = "avatar_{uuid}.png"

COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (33, 150, 243)
COLOR_GREEN = (76, 175, 80)
COLOR_ORANGE = (255, 152, 0)
COLOR_PURPLE = (156, 39, 176)
COLOR_CYAN = (0, 188, 212)
COLOR_DEEP_ORANGE = (255, 87, 34)
COLOR_INDIGO = (63, 81, 181)

AVATAR_BG_PALETTE = [
    COLOR_BLUE,
    COLOR_GREEN,
    COLOR_ORANGE,
    COLOR_PURPLE,
    COLOR_CYAN,
    COLOR_DEEP_ORANGE,
    COLOR_INDIGO,
]

PHONE_PATTERN = r"(8\d{10}|\+7\d{10})"
MSG_PHONE_INVALID = "Введите корректный номер телефона: 8XXXXXXXXXX или +7XXXXXXXXXX"
MSG_PHONE_TAKEN = "Номер телефона уже зарегистрирован"

GITHUB_URL_PATTERN = r"^https?:\/\/(www\.)?github\.com\/[\w\-\.]+(\/[\w\-\.]+)?\/?$"
MSG_GITHUB_INVALID = "Укажите действительную ссылку на репозиторий GitHub"

STATUS_OK = "ok"
STATUS_ERROR = "error"
