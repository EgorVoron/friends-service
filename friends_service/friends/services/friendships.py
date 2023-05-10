from enum import Enum
from typing import Literal

from django.db.models import F, Q, QuerySet

from friends.models import Friendship, FriendshipRequest, User


def get_all(user: User) -> QuerySet | None:
    left_friends, right_friends = [], []
    try:
        left_friends = Friendship.objects.filter(friend_1=user).values_list("friend_2__id", "friend_2__username")
    except FriendshipRequest.DoesNotExist:
        pass
    try:
        right_friends = Friendship.objects.filter(friend_2=user).values_list("friend_1__id", "friend_1__username")
    except FriendshipRequest.DoesNotExist:
        pass
    if not right_friends:
        friends = left_friends
    elif not left_friends:
        friends = right_friends
    else:
        friends = left_friends | right_friends
    return friends


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
    if FriendshipRequest.objects.filter(from_user=cur_user, to_user=other_user).exists():
        return {"success": True, "message": FriendshipStatus.OUTGOING_REQUEST}
    if FriendshipRequest.objects.filter(
            from_user=other_user, to_user=cur_user
    ).exists():
        return {"success": True, "message": FriendshipStatus.INCOMING_REQUEST}
    if Friendship.objects.filter(
            Q(friend_1=cur_user, friend_2=other_user) | Q(friend_1=other_id, friend_2=cur_user)
    ).exists():
        return {"success": True, "message": FriendshipStatus.FRIENDS}
    return {"success": True, "message": FriendshipStatus.UNRELATED}


def delete_friendship(cur_user: User, other_id: int):
    try:
        other_user = User.objects.get(id=other_id)
    except User.DoesNotExist:
        return {"success": False, "message": "user does not exist"}
    left_friendship_exists = Friendship.objects.filter(friend_1=cur_user, friend_2=other_user).exists()
    right_friendship_exists = Friendship.objects.filter(friend_1=other_user, friend_2=cur_user).exists()
    if not left_friendship_exists and not right_friendship_exists:
        return {"success": False, "message": "friendship does not exist"}
    if left_friendship_exists:
        Friendship.objects.filter(friend_1=cur_user, friend_2=other_user).delete()
    else:
        Friendship.objects.filter(friend_1=other_user, frind_2=cur_user).delete()
    return {"success": True, "message": "friendship deleted"}
