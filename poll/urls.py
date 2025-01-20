from django.urls import path
from . import views

app_name = "poll"
urlpatterns = [
    path("vote_form", views.vote_form, name="vote_form"),
    path("vote", views.vote, name="vote"),
    path("vote_result", views.vote_result, name="vote_result"),
]
