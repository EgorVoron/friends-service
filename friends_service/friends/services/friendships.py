from friends.models import User, FriendshipRequest, Friendship
from django.db.models import QuerySet
from django.db.models import Q, F
from enum import Enum
from typing import Literal


def get_all(user: User) -> QuerySet | None:
    right_friends, left_friends = None, None
    try:
        right_friends = Friendship.objects.filter(friend_1=user).values("friend_2").annotate(friend=F("friend_2"))
    except Friendship.DoesNotExist:
        pass
    try:
        left_friends = Friendship.objects.filter(friend_2=user).values("friend_1").annotate(friend=F("friend_1"))
    except Friendship.DoesNotExist:
        pass
    if not right_friends and not left_friends:
        return None

    if not right_friends:
        friends = left_friends
    elif not left_friends:
        friends = right_friends
    else:
        friends = left_friends | right_friends
    friends_ids = list(map(lambda x: x["friend"], friends))
    return User.objects.filter(id__in=friends_ids).values("id", "username")


class FriendshipStatus(str, Enum):
    UNRELATED = "unrelated"
    INCOMING_REQUEST = "incoming"
    OUTGOING_REQUEST = "outgoing"
    FRIENDS = "friends"
    ME = "me"  # it's me


def check_status(cur_user: User, other_id: int):
    if cur_user.id == other_id:
        return {"success": True, "message": FriendshipStatus.ME}
    try:
        other_user = User.objects.get(id=other_id)
    except User.DoesNotExist:
        return {"success": False, "message": "user does not exist"}
    if FriendshipRequest.objects.filter(from_user=cur_user,
                                        to_user=other_user).exists():
        return {"success": True, "message": FriendshipStatus.OUTGOING_REQUEST}
    if FriendshipRequest.objects.filter(from_user=other_user,
                                        to_user=cur_user).exists():
        return {"success": True, "message": FriendshipStatus.INCOMING_REQUEST}
    if Friendship.objects.filter(
            Q(friend_1=cur_user, friend_2=other_user) | Q(friend_1=other_id, friend_2=cur_user)).exists():
        return {"success": True, "message": FriendshipStatus.FRIENDS}
    return {"success": True, "message": FriendshipStatus.UNRELATED}
