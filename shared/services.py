# shared/services.py

from django.contrib.auth.models import Permission
from .models import Notification
from users.models import Role, RolePermission, AppModule

def update_role_permissions(role, permission_ids):
    """Update the permissions for a role."""
    role.permissions.clear()
    for perm_id in permission_ids:
        permission = Permission.objects.get(id=perm_id)
        RolePermission.objects.create(role=role, permission=permission)

def assign_full_app_access(role, app_module):
    """Assign all permissions of an app module to a role."""
    permissions = app_module.get_permissions()
    RolePermission.objects.filter(role=role, app_module=app_module).delete()
    for perm in permissions:
        RolePermission.objects.get_or_create(role=role, permission=perm, app_module=app_module)

def assign_partial_app_access(role, app_module, formset):
    """Assign selected permissions of an app module to a role."""
    RolePermission.objects.filter(role=role, app_module=app_module).delete()
    for form in formset:
        if form.cleaned_data.get('assigned'):
            perm = form.cleaned_data['permission']
            RolePermission.objects.get_or_create(role=role, permission=perm, app_module=app_module)

def create_notification(user, message, notification_type='info'):
    """Create a notification for the user."""
    Notification.objects.create(user=user, message=message, notification_type=notification_type)

def save_app_module(app_module, permissions_data=None):
    """Save an AppModule with or without permissions."""
    app_module.save()
    if not app_module.is_full_app and permissions_data:
        app_module.permissions.clear()
        for perm_data in permissions_data:
            if perm_data.get('assigned'):
                permission = perm_data['permission']
                app_module.permissions.add(permission)