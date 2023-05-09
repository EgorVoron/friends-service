from django.http import HttpResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from friends.serializers import UserNoPasswordSerializer

from friends.services import friendships


@api_view(["GET"])
def ping(request):
    return HttpResponse("pong")


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_friends(request):
    friends = friendships.get_all(request.user)
    if not friends:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UserNoPasswordSerializer(friends, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_status(request):
    other_id = int(request.POST.get("id"))
    result = friendships.check_status(request.user, other_id)
    if result["success"]:
        return Response(status=status.HTTP_200_OK, data=result)
    return Response(status=status.HTTP_404_NOT_FOUND, data=result)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request):
    other_id = int(request.POST.get("id"))
    result = friendships.delete_friendship(request.user, other_id)
    if result["success"]:
        return Response(status=status.HTTP_200_OK, data=result)
    return Response(status=status.HTTP_404_NOT_FOUND, data=result)
