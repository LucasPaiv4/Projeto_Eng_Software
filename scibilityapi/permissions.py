from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada para permitir apenas que o criador do projeto possa editá-lo.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permissões de escrita são apenas permitidas ao criador do projeto.
        return obj.usuario == request.user
