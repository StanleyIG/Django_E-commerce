# from collections import OrderedDict
# from urllib.parse import urlencode, urlunparse


# url = urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')), v='5.92'))
# api_url = urlunparse(
#             ('https',
#              'api.vk.com',
#              '/method/users.get',
#              None,
#              urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')), v='5.92')),
#              None
#              )
#         )

# print(url) 
# print(api_url) 
# print(OrderedDict(fields=','.join(('bdate', 'sex', 'about'))))     