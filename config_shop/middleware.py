from django.core.cache import cache
from django.http import HttpRequest


class CacheIpAddressMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        count = 0
        # Проверяем, является ли request объектом HttpRequest и является ли пользователь анонимным
        if isinstance(request, HttpRequest) and request.user.is_anonymous:
            ip_address = cache.get(f'anonymous_user_ip_address_{request.META["REMOTE_ADDR"]}')
            if ip_address:
                if ip_address[1] < 1:
                    count += 1
                    cache.set(f'anonymous_user_ip_address_{request.META["REMOTE_ADDR"]}',
                              (request.META['REMOTE_ADDR'], count),
                              timeout=100)
            else:
                cache.set(f'anonymous_user_ip_address_{request.META["REMOTE_ADDR"]}',
                          (request.META['REMOTE_ADDR'], count),
                          timeout=100)
                                                

        response = self.get_response(request)
        return response
