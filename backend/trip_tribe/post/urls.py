from django.urls import path

from . import api


urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('<uuid:pk>/delete/', api.post_delete, name='post_delete'),
    path('<uuid:pk>/report/', api.post_report, name='post_report'),
    path('profile/<uuid:id>/', api.post_list_profile, name='post_list_profile'),
    path('create/', api.post_create, name='post_create'),
]