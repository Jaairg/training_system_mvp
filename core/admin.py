from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Roles)
admin.site.register(Workcenter)
admin.site.register(CFETP)
admin.site.register(MTL)
admin.site.register(ITP)
admin.site.register(Ranks)
admin.site.register(AFSC)

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'workcenter', 'afsc', 'skill_level', 'rank')
    search_fields = ('name',)
    list_filter = ('name', 'role', 'workcenter', 'afsc', 'skill_level', 'rank')
