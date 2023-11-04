from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("createNewPage", views.createNewPage, name="newPage"),
    path("random", views.randomPage, name="random"),
    # path("<str:tosearch>", views.results, name="results"),
    path("wiki/<str:tosearch>", views.results, name="results"),
    # path("createNewPage", views.createNewPage, name="newPage")
]