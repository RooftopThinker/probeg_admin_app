from django.contrib import admin
from django.urls import path
from monitor.views import test
urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test, name='receive_payment'),
    path('/', admin.site.urls),
]
