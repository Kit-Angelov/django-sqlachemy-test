from django.utils.deprecation import MiddlewareMixin
from users.core import authorize
from django.http import JsonResponse


class PermissionMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func.__name__ == "_allow_any":
            return view_func(request, *view_args, **view_kwargs)
        else:
            headers = request.headers
            access_token = headers.get('Authorization')
            user = authorize(access_token)
            if user:
                request.user = user
            else:
                return JsonResponse({'error': 'unauthorized'}, status=403)
        return None


def allow_any(f):
    def _allow_any(*args, **kwargs):
        return f(*args, **kwargs)
    return _allow_any
