from django.contrib import admin

from .models import Demand, DemandHistory


@admin.register(Demand)
class DemandAdmin(admin.ModelAdmin):
    list_display = (
        'credit_cwallet', 'credit_transaction', 'release_datetime', 'status', 'demand_remain', 'demand_balance',
        'created_at', 'updated_at',)


# admin.site.register(Demand, DemandAdmin)
@admin.register(DemandHistory)
class DemandHistoryAdmin(admin.ModelAdmin):
    list_display = ("demand", "amount", "status")
# admin.site.register(DemandHistory)
