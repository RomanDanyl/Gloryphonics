from django.contrib import admin

from user.models import (
    User,
    RegistrationApplication,
)

admin.site.register(RegistrationApplication)
admin.site.register(User)


# @admin.register(User)
# class UserAdmin(DjangoUserAdmin):
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         (
#             _("Personal info"),
#             {
#                 "fields": (
#                     "first_name",
#                     "last_name",
#                     "avatar",
#                     "country",
#                     "description",
#                     "slogan",
#                     "genres",
#                 )
#             },
#         ),
#         (
#             _("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "groups",
#                     "user_permissions",
#                     "role",
#                 )
#             },
#         ),
#         (_("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("email", "password1", "password2"),
#             },
#         ),
#     )
#     list_display = ("email", "first_name", "last_name", "is_staff")
#     search_fields = ("email", "first_name", "last_name")
#     ordering = ("email",)
