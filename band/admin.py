from django.contrib import admin

from band.forms import BandAdminForm
from band.models import (
    BandImage,
    Follower,
    Album,
    SocialLinks,
    Genre,
    Comment,
    BandVideo,
    Band,
)
from user.models import User

admin.site.register(BandImage)
admin.site.register(BandVideo)
admin.site.register(Follower)
admin.site.register(Album)
admin.site.register(SocialLinks)
admin.site.register(Genre)
admin.site.register(Comment)


class BandImageInline(admin.TabularInline):
    model = BandImage
    extra = 1
    fields = ("image",)


class BandVideoInline(admin.TabularInline):
    model = BandVideo
    extra = 1


class SocialLinksInline(admin.StackedInline):
    model = SocialLinks
    can_delete = True


class AlbumInline(admin.TabularInline):
    model = Album
    extra = 1


class MembersInline(admin.TabularInline):
    model = User
    extra = 1


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    form = BandAdminForm
    list_display = ("name", "country", "description", "slogan", "cover_image")
    search_fields = ("name", "country")
    inlines = [BandImageInline, BandVideoInline, SocialLinksInline]
