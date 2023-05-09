from friends.models import User, FriendshipRequest, Friendship
from django.db.models import QuerySet, Q
from typing import Literal


def get_incoming(from_user: User) -> QuerySet | None:
    try:
        queryset: QuerySet = FriendshipRequest.objects.filter(from_user=from_user)
    except FriendshipRequest.DoesNotExist:
        return None
    return queryset


def get_outgoing(to_user: User) -> QuerySet | None:
    try:
        queryset: QuerySet = FriendshipRequest.objects.filter(to_user=to_user)
    except FriendshipRequest.DoesNotExist:
        return None
    return queryset


def send(from_user: User, to_id: int):
    try:
        to_user: User = User.objects.get(id=to_id)
    except User.DoesNotExist:
        return {"success": False, "message": "user does not exist"}
    if FriendshipRequest.objects.filter(from_user=from_user,
                                       to_user=to_user).exists():
        return {"success": False, "message": "request already exists"}
    if Friendship.objects.filter(Q(friend_1=from_user, friend_2=to_user) | Q(friend_1=to_user, friend_2=from_user)).exists():
        return {"success": False, "message": "friendship already exists"}
    if FriendshipRequest.objects.filter(from_user=to_user,
                                        to_user=from_user).exists():
        FriendshipRequest.objects.filter(from_user=to_user,
                                         to_user=from_user).delete()
        Friendship(friend_1=to_user, friend_2=from_user).save()
        return {"success": True, "message": "friendship created"}
    FriendshipRequest(from_user=from_user, to_user=to_user).save()
    return {"success": True, "message": "friendship request created"}
