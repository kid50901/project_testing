from django.contrib import admin
from covid19BotApp.models import covid7dayInfo
# Register your models here.
class myAdminDRimgtable(admin.ModelAdmin):
	list_display=("location","date")
admin.site.register(covid7dayInfo,myAdminDRimgtable)