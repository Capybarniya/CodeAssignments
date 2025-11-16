"""
URL configuration for starwars_ships project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ships import views

ships = [
    path('1', views.starship_card, kwargs={"starship_id":2}),
    path('2', views.starship_card, kwargs={"starship_id":3}),
    path('3', views.starship_card, kwargs={"starship_id":5}),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('starships/', include(ships)),
]
