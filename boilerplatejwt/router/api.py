from django.conf.urls import include
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from boilerplatejwt.router.api_v1_0 import api_v1_0_urls

api_urls = [
    path('v1/', include((api_v1_0_urls, 'api_v1_0_urls'), namespace='v1.0')),
    path('login/', obtain_auth_token, name='login')
]
