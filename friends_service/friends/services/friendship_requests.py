from django.db.models import Q, QuerySet

from friends.models import Friendship, FriendshipRequest, User


def get_incoming(to_user: User) -> QuerySet | None:
    try:
        queryset: QuerySet = FriendshipRequest.objects.filter(to_user=to_user).values_list("to_user__id",
                                                                                           "to_user__username")
    except FriendshipRequest.DoesNotExist:
        return None
    return queryset


def get_outgoing(from_user: User) -> QuerySet | None:
    try:
        queryset: QuerySet = FriendshipRequest.objects.filter(from_user=from_user).values_list("from_user__id",
                                                                                               "from_user__username")
    except FriendshipRequest.DoesNotExist:
        return None
    return queryset


def send(from_user: User, to_id: int):
    if from_user.id == to_id:
        return {"success": False, "message": "cannot befriend myself"}
    try:
        to_user: User = User.objects.get(id=to_id)
    except User.DoesNotExist:
        return {"success": False, "message": "user does not exist"}
    if FriendshipRequest.objects.filter(from_user=from_user,
                                        to_user=to_user).exists():
        return {"success": False, "message": "request already exists"}
    if Friendship.objects.filter(
            Q(friend_1=from_user, friend_2=to_user) | Q(friend_1=to_user, friend_2=from_user)).exists():
        return {"success": False, "message": "friendship already exists"}
    if FriendshipRequest.objects.filter(from_user=to_user,
                                        to_user=from_user).exists():
        FriendshipRequest.objects.filter(from_user=to_user,
                                         to_user=from_user).delete()
        Friendship(friend_1=to_user, friend_2=from_user).save()
        return {"success": True, "message": "friendship created"}
    FriendshipRequest(from_user=from_user, to_user=to_user).save()
    return {"success": True, "message": "friendship request created"}


def accept(from_user: User, to_id: int):
    try:
        to_user: User = User.objects.get(id=to_id)
    except User.DoesNotExist:
        return {"success": False, "message": "user does not exist"}
    if not FriendshipRequest.objects.filter(from_user=from_user,
                                            to_user=to_user).exists():
        return {"success": False, "message": "friendship request does not exist"}
    # here friendship request exists. I remove it and create new friendship
    FriendshipRequest.objects.filter(from_user=from_user, to_user=to_user).delete()
    Friendship(friend_1=from_user, friend_2=to_user).save()
    return {"success": True, "message": "friendship request accepted"}


def decline(from_user: User, to_id: int):
    try:
        to_user: User = User.objects.get(id=to_id)
    except User.DoesNotExist:
        return {"success": False, "message": "user does not exist"}
    if not FriendshipRequest.objects.filter(from_user=from_user,
                                            to_user=to_user).exists():
        return {"success": False, "message": "friendship request does not exist"}
    # here friendship request exists. I remove it.
    FriendshipRequest.objects.filter(from_user=from_user, to_user=to_user).delete()
    return {"success": True, "message": "friendship request declined"}
