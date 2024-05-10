from django.contrib import admin
from django.urls import path, include
from user import urls, views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('odontograma/', include('odontograma.urls')),
    path('user/', include('user.urls')),
    path('person/', include('person.urls')),
    path('', views.login_view)
]
