from django.contrib import admin
from myapp.models import  assets,debt,income,endMeets
# Register your models here.
class myAdminDRimgtable(admin.ModelAdmin):
	list_display=("date","account")
class myAdminDRimgtable_income(admin.ModelAdmin):
	list_display=("date","income_type")
class myAdminDRimgtable_endmeets(admin.ModelAdmin):
	list_display=("owner","year_month")

admin.site.register(assets,myAdminDRimgtable)
admin.site.register(debt,myAdminDRimgtable)
admin.site.register(income,myAdminDRimgtable_income)
admin.site.register(endMeets,myAdminDRimgtable_endmeets)