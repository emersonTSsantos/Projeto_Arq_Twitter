from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Meep, UserProfile

# Unregister Groups
admin.site.unregister(Group)

# Mix Profile info into User info
class UserProfileInline(admin.StackedInline):
    model = UserProfile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Just display username field on admin page
    fields = ['username']
    inlines = [UserProfileInline]

# Unregister initial User
admin.site.unregister(User)

# Reregister User and Profile
admin.site.register(User, UserAdmin)
# admin.site.register(UserProfile)

# Register Meeps model
admin.site.register(Meep)
