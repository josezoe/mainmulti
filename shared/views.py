from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from shared.models import Role, RolePermission, Notification  # Assuming Notification is in shared app


@login_required
def assign_permissions_to_role(request, role_id):
    if request.user.user_type != 'vendor':
        raise PermissionDenied("Access denied.")

    role = Role.objects.get(id=role_id, vendor=request.user)

    if request.method == 'POST':
        permission_ids = request.POST.getlist('permissions')
        role.permissions.clear()
        for perm_id in permission_ids:
            permission = Permission.objects.get(id=perm_id)
            RolePermission.objects.create(role=role, permission=permission)
        
        return redirect('role_detail', role_id=role.id)

    all_permissions = Permission.objects.all()
    role_permissions = role.permissions.values_list('permission__id', flat=True)
    return render(request, 'assign_permissions.html', {
        'role': role,
        'all_permissions': all_permissions,
        'role_permissions': role_permissions
    })


def create_notification(user, message, notification_type='info'):
    Notification.objects.create(user=user, message=message, notification_type=notification_type)