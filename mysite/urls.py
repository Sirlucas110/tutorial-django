"""
URL configuration for mysite project.

A lista `urlpatterns` encaminha URLs para visualizações. Para mais informações, consulte:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Adicione uma importação: from my_app import views
    2. Adicione uma URL para urlpatterns: path('', views.home, name='home')
Class-based views
    1. Adicione uma importação: from other_app.views import Home
    2. Adicione uma URL para urlpatterns: path('', Home.as_view(), name='home')
Including another URLconf
    1. Importe a função include(): from django.urls import include, path
    2. Adicione uma URL para urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    path('admin/', admin.site.urls),
]
