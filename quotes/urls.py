from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('search', views.search, name='search'),
    path('login', views.login_view, name='login'),
    path('addData', views.addData, name='addData'),
    path('contact', views.contact, name='contact'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('display/<int:n>', views.display, name='display'),
    path('allquotes/<int:page>', views.allquotes, name='allquotes'),
]
