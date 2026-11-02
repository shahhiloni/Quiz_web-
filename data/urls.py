
from django.urls import path
from . import views

app_name = "quiz"

urlpatterns = [
    path("", views.categories, name="categories"),
    path("quiz/<int:category_id>/", views.start_quiz, name="start_quiz"),
]
