from django.contrib import admin

from credit_card.credit_commission_settings.models import CreditCommissionSetting


class CreditCommissionSettingAdmin(admin.ModelAdmin):
    list_display = ["credit_marketer", "type", "receiver", "club", "quantity"]
    list_filter = ["credit_marketer", "type", ]
    date_hierarchy = 'created_at'


admin.site.register(CreditCommissionSetting, CreditCommissionSettingAdmin)
