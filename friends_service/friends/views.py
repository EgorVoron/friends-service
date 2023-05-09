from django.http import HttpResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from friends.services import friendship_requests, friendships
from friends.serializers import FriendshipRequestsSerializer, UserNoPasswordSerializer


@api_view(["GET"])
def ping(request):
    return HttpResponse("pong")


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def incoming_requests(request):
    requests = friendship_requests.get_incoming(request.user)
    if not requests:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = FriendshipRequestsSerializer(requests, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def outgoing_requests(request):
    requests = friendship_requests.get_outgoing(request.user)
    if not requests:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = FriendshipRequestsSerializer(requests, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_request(request):
    result = friendship_requests.send(request.user, request.POST.get("to_id"))
    if result["success"]:
        return Response(status=status.HTTP_201_CREATED, data=result)
    return Response(status=status.HTTP_400_BAD_REQUEST, data=result)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_friends(request):
    friends = friendships.get_all(request.user)
    print(friends)
    if not friends:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UserNoPasswordSerializer(friends, many=True)
    return Response(serializer.data)
