from friends.models import User, FriendshipRequest, Friendship
from django.db.models import QuerySet
from django.db.models import Q, F


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
