from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("create", views.user_create, name="create"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("detail", views.user_detail, name="detail"),
    path("update", views.user_update, name="update"),
    path("pwd_change", views.pwd_change, name="pwd_change"),
    path("delete", views.user_delete, name="delete"),
]
