from django.contrib import admin

from .models import Friendship, FriendshipRequest

# Register your models here.

admin.site.register(FriendshipRequest)
admin.site.register(Friendship)