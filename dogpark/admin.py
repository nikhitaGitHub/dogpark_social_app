from django.contrib import admin
from dogpark.models import FriendRequest, Owner, Dog, Friendship, Events, Goals, Ratings

admin.site.register(FriendRequest)
admin.site.register(Owner)
admin.site.register(Dog)
admin.site.register(Friendship)
admin.site.register(Events)
admin.site.register(Goals)
admin.site.register(Ratings)
# Register your models here.
