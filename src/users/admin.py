from django.contrib import admin
from .models import Remainder, RemainderTask
# Register your models here

class RemainderAdmin(admin.ModelAdmin):
	readonly_fields = ('created_at', 'modified_at', )

admin.site.register(Remainder, RemainderAdmin)
admin.site.register(RemainderTask)
