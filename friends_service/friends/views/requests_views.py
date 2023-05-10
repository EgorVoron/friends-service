from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from friends.serializers import serialize_user_info
from friends.services import friendship_requests


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def incoming_requests(request):
    requesters = friendship_requests.get_incoming(request.user)
    if not requesters:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(serialize_user_info(requesters))


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def outgoing_requests(request):
    requested = friendship_requests.get_outgoing(request.user)
    if not requested:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(serialize_user_info(requested))


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_request(request):
    result = friendship_requests.send(request.user, int(request.POST.get("to_id")))
    if result["success"]:
        return Response(status=status.HTTP_201_CREATED, data=result)
    return Response(status=status.HTTP_400_BAD_REQUEST, data=result)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def accept(request):
    result = friendship_requests.accept(request.user, int(request.POST.get("to_id")))
    if result["success"]:
        return Response(status=status.HTTP_201_CREATED, data=result)
    return Response(status=status.HTTP_400_BAD_REQUEST, data=result)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def decline(request):
    result = friendship_requests.decline(request.user, int(request.POST.get("to_id")))
    if result["success"]:
        return Response(status=status.HTTP_201_CREATED, data=result)
    return Response(status=status.HTTP_400_BAD_REQUEST, data=result)
