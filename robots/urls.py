from django.urls import include, path

from .views import create_robot


urlpatterns = [
    path('add_robot/', create_robot, name='add_robot'),
]
