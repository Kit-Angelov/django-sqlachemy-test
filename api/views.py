from django.http import JsonResponse
from users.middleware.permission import allow_any
from users.core import authorize


@allow_any
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        return JsonResponse('')
