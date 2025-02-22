from django.contrib import admin
from django.urls import path
from monitor.views import accept_payment
urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/', accept_payment, name='receive_payment'),
    path('', admin.site.urls),
]
