from rest_framework import permissions
from api.models import Terapeutas, Tutor, Role


def _has_role(user, role_name):
    """Check role on custom Usuario model; fall back to Django's is_superuser."""
    if getattr(user, 'is_superuser', False):
        return True
    return hasattr(user, 'roles') and user.roles.filter(nombre__iexact=role_name).exists()


class IsAdminUser(permissions.BasePermission):
    """Permite acceso solo a usuarios con rol de administrador."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and
                    _has_role(request.user, 'admin'))


class IsTerapeuta(permissions.BasePermission):
    """Permite acceso solo a usuarios con rol de terapeuta."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and
                    _has_role(request.user, 'terapeuta'))

    def has_object_permission(self, request, view, obj):
        if getattr(request.user, 'is_superuser', False):
            return True
        if hasattr(obj, 'terapeuta_id'):
            return Terapeutas.objects.filter(usuario_id=request.user.id).exists()
        return True


class IsTutor(permissions.BasePermission):
    """Permite acceso solo a usuarios con rol de tutor."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and
                    _has_role(request.user, 'tutor'))

    def has_object_permission(self, request, view, obj):
        if getattr(request.user, 'is_superuser', False):
            return True
        if hasattr(obj, 'usuario_id'):
            return obj.usuario_id == request.user.id
        if hasattr(obj, 'tutor_id'):
            return obj.tutor_id.usuario_id == request.user.id
        return True


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permite a propietarios editar sus objetos."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.usuario_id == request.user.id if hasattr(obj, 'usuario_id') else False


class CanManageUsers(permissions.BasePermission):
    """Permite solo a administradores crear, editar o eliminar usuarios."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_authenticated and
                    _has_role(request.user, 'admin'))


class CanManageSessions(permissions.BasePermission):
    """Permite a terapeutas crear/editar solo sus sesiones. Admin puede manejar todas."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if _has_role(request.user, 'admin'):
            return True
        if _has_role(request.user, 'terapeuta'):
            if hasattr(obj, 'terapeuta_id'):
                terapeuta = Terapeutas.objects.filter(usuario_id=request.user.id).first()
                return obj.terapeuta_id == terapeuta
        return request.method in permissions.SAFE_METHODS


class CanManagePacients(permissions.BasePermission):
    """Permite a tutores ver solo sus pacientes. Admin puede manejar todos."""
    def has_object_permission(self, request, view, obj):
        if _has_role(request.user, 'admin'):
            return True
        if _has_role(request.user, 'tutor'):
            tutor = Tutor.objects.filter(usuario_id=request.user.id).first()
            return obj.tutor_id == tutor
        return request.method in permissions.SAFE_METHODS
