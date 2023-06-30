NUMBER_OF_CHARS: int = 15

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
SUPERUSER = 'superuser'
ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
    (SUPERUSER, 'Суперюзер'),
)
