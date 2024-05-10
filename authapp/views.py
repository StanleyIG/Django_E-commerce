from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from authapp.forms import RegistrationForm
from django.contrib import auth
from django.views.decorators.cache import cache_page
from mainapp.views import index
from django.contrib.auth.hashers import make_password
# Create your views here.

#@csrf_exempt
# def registration(request):
#     if request.method == 'POST':
#         print(request.POST)
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         return JsonResponse({'message': 'ok'})
#     else:
#         # GET-запрос, отображаем форму регистрации
#         return render(request, 'authapp/registr.html')

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return JsonResponse({'message': 'ok'})
        else:
            return JsonResponse({'errors': form.errors})
    else:
        return render(request, 'authapp/registr.html')



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        # аутентификация пользователя
        # аутентификация пользователя
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            print(user)
            auth.login(request, user)
        else:
            print('asfsdf')
            return JsonResponse({'error': 'Неверный логин или пароль'})
        # return redirect(reverse('mainapp:index'))
        return JsonResponse({'message': 'ok'})
    else:
        return render(request, 'authapp/registr.html')


     

    #     else:
    #         return JsonResponse({'error': 'Неверный логин или пароль'})
    # else:
    #     return render(request, 'authapp/registr.html')
