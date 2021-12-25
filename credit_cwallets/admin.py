from django.contrib import admin

from .models import CreditCwallet


# admin.site.register(CreditCwallet)

@admin.register(CreditCwallet)
class CreditCwalletAdmin(admin.ModelAdmin):
    list_display = ("cwallet", "current_cashtag", "credit_amount", "balance", "credit_marketer", "status", "is_demand",
                    "demand_setting", "checkout_period_month")
