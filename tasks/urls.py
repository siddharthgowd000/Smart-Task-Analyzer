from django.urls import path
from . import views

urlpatterns = [
    path("analyze/", views.analyze_view, name="analyze_tasks"),
    path("suggest/", views.suggest_view, name="suggest_tasks"),
]
