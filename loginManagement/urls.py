from django.conf.urls import url, include
from django.urls import path


from . import views

app_name = 'loginManagement'

urlpatterns = [
    path(r'', views.index,name="index"),
    path(r'login/', views.login,name="login"),
    path(r'register/', views.register, name="register"),
    path(r'logout/', views.logout, name="logout")
]