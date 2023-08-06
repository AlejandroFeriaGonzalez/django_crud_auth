from django.contrib import admin

from tasks.models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


# admin.site.register(Task, TaskAdmin)
