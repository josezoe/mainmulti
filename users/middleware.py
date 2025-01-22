# In a new file like middleware.py

from ipware import get_client_ip

class UpdateUserIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if hasattr(request, 'user') and request.user.is_authenticated:
            ip, _ = get_client_ip(request)
            if ip:
                request.user.last_known_ip = ip
                request.user.save(update_fields=['last_known_ip'])
        return response