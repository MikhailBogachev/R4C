from django.urls import include, path

from .views import create_order


urlpatterns = [
    path('create_order/', create_order, name='create_order'),
]
