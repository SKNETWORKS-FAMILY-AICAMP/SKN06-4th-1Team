from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("create", views.create, name="create"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("detail", views.detail, name="detail"),
    path("update", views.update, name="update"),
    path("pwd_change", views.pwd_change, name="pwd_change"),
    path("delete", views.delete, name="delete"),
]