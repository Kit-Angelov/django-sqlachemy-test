from django.http import JsonResponse
from users.middleware.permission import allow_any
from users.core import login as user_login
from users.core import logout as user_logout


@allow_any
def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'not allowed'}, status=405)
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = user_login(email, password)

    response_data = {
        'access_token': user.auth_token.access_token,
        'refresh_token': user.auth_token.refresh_token
    }
    return JsonResponse(response_data)


def logout(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'not allowed'}, status=405)
    user_logout(request.user)
    return JsonResponse({})