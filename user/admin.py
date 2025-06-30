from django.contrib import admin

from user.models import User, UserImage, RegistrationApplication, Follower, Album

admin.site.register(User)
admin.site.register(UserImage)
admin.site.register(RegistrationApplication)
admin.site.register(Follower)
admin.site.register(Album)