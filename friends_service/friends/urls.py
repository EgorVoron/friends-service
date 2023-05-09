from django.urls import include, path
from rest_framework import routers

from friends import views

# requests_router = routers.DefaultRouter()
# requests_router.register(r'incoming', views.incoming_requests, basename='incoming')

urlpatterns = [
    path('requests/incoming', views.incoming_requests),
    path('requests/outgoing', views.outgoing_requests),
    path('requests/send', views.send_request),
    path('requests/accept', views.accept),
    path('requests/decline', views.decline),

    path('all', views.all_friends),
    path('check_status', views.check_status),
    path('delete', views.delete)
]
