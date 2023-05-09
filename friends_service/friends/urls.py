from django.urls import path
from friends import views

from django.urls import path, include
from rest_framework import routers

# requests_router = routers.DefaultRouter()
# requests_router.register(r'incoming', views.incoming_requests, basename='incoming')

urlpatterns = [
    path('requests/incoming', views.incoming_requests),
    path('requests/outgoing', views.outgoing_requests),
    path('requests/send', views.send_request),

    path('all', views.all_friends)
]
