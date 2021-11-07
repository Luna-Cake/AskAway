from django.urls import include, path
from .views import index

urlpatterns = [
    path('', index),
    path('host/<str:session_code>', index),
    path('participant', index),
    path('join-session', index),
    path('session/<str:session_code>', index),
    path('error', index)
]
