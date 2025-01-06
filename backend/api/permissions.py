from rest_framework import permissions


class ReadOrAuthenticated(permissions.BasePermission):
    """
    Класс разрешений на получение, создание, обновление, удаление 'Breed'.

    Аноним может только смотреть;
    аутентифицированный пользователь: смотреть, создавать, менять
    и удалять свой контент.

    Возвращает:
        True или False: в зависимости от наличия разрешения.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or request.user.is_authenticated
        )


class ReadOrAuthenticatedOrOwner(ReadOrAuthenticated):
    """
    Класс разрешений на получение, создание, обновление, удаление 'Породы'.

    Расширяет ReadOrAuthenticated чтобы убедиться что только хозяин мог менять, удалять 'Dog'.

    Возвращает:
        True или False: в зависимости от наличия разрешения.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and obj.owner == request.user
        )
