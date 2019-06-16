from django.http import JsonResponse


def me(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'not allowed'}, status=405)
    user = request.user
    response_data = {
        'first_name': user.first_name,
        'second_name': user.second_name,
        'patronymic': user.patronymic,
        'email': user.email,
        'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d'),
        'city': user.city.name
    }
    return JsonResponse(response_data)