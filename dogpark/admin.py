from django.contrib import admin
from dogpark.models import FriendRequest, Owner, Dog, Friendship

admin.site.register(FriendRequest)
admin.site.register(Owner)
admin.site.register(Dog)
admin.site.register(Friendship)
# Register your models here.
