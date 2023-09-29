from django.urls import include, path

from .views import create_robot, download_production_list


urlpatterns = [
    path('add_robot/', create_robot, name='add_robot'),
    path('download/', download_production_list, name='download_production_list'),
]
