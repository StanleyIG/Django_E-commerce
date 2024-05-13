from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import RedirectView

# Create your views here.


def index(request):
    # return render(request, 'mainapp/index.html')
    url_1 = reverse('mainapp:index')
    url_2 = reverse_lazy('mainapp:about')
    # url_3 = reverse('mainapp:none') 
    # reverse вычисляет url сразу, даже если он не будет использоваться, и соответсвенно выбросится ошибка, т.к. шаблон url не определён в urls.py
    url_3 = reverse_lazy('mainapp:none') # ложный адрес которого нет в URLconf.
    # reverse_lazy вычисляет url лениво, и если его не вызвать, то ошибок не будет, но если например попробовать напечатать, то выбросится ошибка
    # print(url_3)

    # Допустим ситуация когда есть какая-то проверка (валидация входящих данных, иная логика) 
    # и ветвление, где есть разный исход результат выполнения view, и каждый 
    # исход в зависимости от логики предcтавления редиректает на разные адреса.
    # Получается что есть смысл использовать reverse_lazy для оптимизации выполнения view, что-бы избежать постоянных ненужных 
    # вычислений url которые могут быть не вызваны 


    return HttpResponse('URL1=%s & URL2=%s' % (url_1, url_2))


def about(request):
    url = reverse_lazy('mainapp:index')
    return redirect(url)
    #return HttpResponse(url)
    # return render(request, 'mainapp/about.html')
