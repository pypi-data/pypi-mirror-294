from django.contrib import admin
from dbtimer.models import DBTimerHistory, DBTimerHelper

class DBTimerHelperInline(admin.TabularInline):
    model=DBTimerHelper
    extra=0

@admin.register(DBTimerHistory)
class DBTimerHistoryAdmin(admin.ModelAdmin):
    list_display = ["pk", "created_at"]
    inlines=[DBTimerHelperInline]
