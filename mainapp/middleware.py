from audioop import reverse
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        # return JsonResponse({
        #     'status': 'error',
        #     'message': str(exception),
        #     'time': timezone.now()
        # })
        # return redirect('/mainapp/')
        context = {
            'error': f'{timezone.now().strftime("%d.%m.%Y:%H:%M")}\
                Произошла ошибка. Повторите попытку позже.'
        }
        # либо отрендерить какую нибудь страницу с ошибкой
        return render(request, 'error_pages/page_500.html', context=context)

                
