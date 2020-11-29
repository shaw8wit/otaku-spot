from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('search', views.search, name='search'),
    path('login', views.login_view, name='login'),
    path('display', views.display, name='display'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
]
