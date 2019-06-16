from django.http import JsonResponse
from users.middleware.permission import allow_any
from users.core import login as user_login
from users.core import logout as user_logout
from users.core import refresh_token as user_refresh_token


@allow_any
def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'not allowed'}, status=405)
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = user_login(email, password)

    response_data = {
        'access_token': user.auth_token.access_token,
        'first_name': user.first_name,
        'second_name': user.second_name,
        'patronymic': user.patronymic,
        'email': user.email,
        'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d'),
        'city': user.city.name
    }
    return JsonResponse(response_data)


def logout(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'not allowed'}, status=405)
    user_logout(request.user)
    return JsonResponse({})


@allow_any
def refresh_token(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'not allowed'}, status=405)
    access_token = request.POST.get('access_token')
    new_access_token = user_refresh_token(access_token)
    if new_access_token:
        response_data = {
            'access_token': new_access_token
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'invalid access token'}, status=403)
