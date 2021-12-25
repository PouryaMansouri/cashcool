from django.contrib import admin

from .models import CreditTransaction


# admin.site.register(CreditTransaction)

@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "amount", "ptc", "error_explanation", "commission_transaction", "status",
                    "commission_transaction_parent")
