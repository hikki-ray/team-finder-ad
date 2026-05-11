MAX_NAME_LENGTH = 32
MAX_SURNAME_LENGTH = 32
MAX_PHONE_LENGTH = 12
MAX_ABOUT_LENGTH = 512

FILTER_FAVORITE_AUTHORS = "owners-of-favorite-projects"
FILTER_PARTICIPATING_AUTHORS = "owners-of-participating-projects"
FILTER_INTERESTED_USERS = "interested-in-my-projects"
FILTER_MY_PARTICIPANTS = "participants-of-my-projects"

FILTER_OPTIONS = (
    (FILTER_FAVORITE_AUTHORS, "Авторы избранных проектов"),
    (FILTER_PARTICIPATING_AUTHORS, "Авторы проектов, в которых я участвую"),
    (FILTER_INTERESTED_USERS, "Пользователи, которым нравятся мои проекты"),
    (FILTER_MY_PARTICIPANTS, "Участники моих проектов"),
)

MSG_INVALID_VALUES = "Неверный Email или пароль"

MSG_GITHUB_TAKEN = "Профиль с данной ссылкой на GitHub уже существует"

MSG_EMAIL_TAKEN = "Пользователь с таким Email уже существует"
MSG_EMAIL_REQUIRED = "Поле Email должно быть заполнено"

MSG_SUPERUSER_STAFF = "Суперпользователь должен иметь is_staff=True"
MSG_SUPERUSER_SUPERUSER = "Суперпользователь должен иметь is_superuser=True"

RESPONSE_MSG_NOT_FOUND = "Профиль не найден"
