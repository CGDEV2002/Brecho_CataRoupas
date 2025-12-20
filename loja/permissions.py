from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada para permitir apenas aos proprietários 
    editar seus próprios objetos.
    """
    def has_object_permission(self, request, view, obj):
        # Permissões de leitura para qualquer request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permissões de escrita apenas para o proprietário do objeto
        return obj.owner == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada para permitir apenas a admins
    criar/editar/deletar objetos.
    """
    def has_permission(self, request, view):
        # Permissões de leitura para qualquer request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permissões de escrita apenas para admins
        return request.user and request.user.is_staff
