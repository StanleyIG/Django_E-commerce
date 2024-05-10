from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from authapp.forms import RegistrationForm, LoginForm
from django.contrib import auth
from django.views.decorators.cache import cache_page
from mainapp.views import index
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
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
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(email=email, password=password)
            if user:
                auth.login(request, user)
                # return redirect(reverse('mainapp:index'))
                return JsonResponse({'message': render_to_string('mainapp/index.html')})
            else:
                return JsonResponse({'error': 'Неверный логин или пароль'})
                                
        # # аутентификация пользователя
        # # аутентификация пользователя
        # user = auth.authenticate(password=password, email=email)
        # if user is not None:
        #     print(user)
        #     auth.login(request, user)
        # else:
        #     print('asfsdf')
        #     return JsonResponse({'error': 'Неверный логин или пароль'})
        # # return redirect(reverse('mainapp:index'))
        # return JsonResponse({'message': 'ok'})
    else:
        return render(request, 'authapp/registr.html')


     

    #     else:
    #         return JsonResponse({'error': 'Неверный логин или пароль'})
    # else:
    #     return render(request, 'authapp/registr.html')
