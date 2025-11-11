from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext as _

from user.models import (
    User,
    UserImage,
    RegistrationApplication,
    Follower,
    Album,
    SocialLinks,
    Genre,
    Comment,
    UserVideo,
)

admin.site.register(UserImage)
admin.site.register(RegistrationApplication)
admin.site.register(Follower)
admin.site.register(Album)
admin.site.register(SocialLinks)
admin.site.register(Genre)
admin.site.register(Comment)


class UserImageInline(admin.TabularInline):
    model = UserImage
    extra = 1


class UserVideoInline(admin.TabularInline):
    model = UserVideo
    extra = 1


class SocialLinksInline(admin.StackedInline):
    model = SocialLinks
    can_delete = True


class AlbumInline(admin.TabularInline):
    model = Album
    extra = 1


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                    "country",
                    "description",
                    "slogan",
                    "genres",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "role",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    inlines = (
        AlbumInline,
        UserImageInline,
        UserVideoInline,
        SocialLinksInline,
    )
