from django.contrib import admin

from user.models import User, UserImage, RegistrationApplication

admin.site.register(User)
admin.site.register(UserImage)
admin.site.register(RegistrationApplication)
