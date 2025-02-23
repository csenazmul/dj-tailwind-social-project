from django.urls import path
from . import views  # Ensure views is properly imported

urlpatterns = [
    path('', views.index, name='index'),  # Example route
]
