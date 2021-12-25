from django.contrib import admin

from .models import Debt, DebtHistory, DebtPenalty


@admin.register(Debt)
class DebtCreditAdmin(admin.ModelAdmin):
    list_display = ["credit_cwallet", "credit_transaction", 'repayment_date_time', "status",
                    "debt_remain", "all_debt_remain", "created_at"]
    date_hierarchy = 'created_at'


@admin.register(DebtHistory)
class DebtHistoryCreditCwalletAdmin(admin.ModelAdmin):
    list_display = ("debt_credit_cwallet", "repayment_debt_transaction", "amount")


# admin.site.register(Debt, DebtCreditAdmin)

@admin.register(DebtPenalty)
class DebtPenaltyAdmin(admin.ModelAdmin):
    list_display = ('debt', 'penalty_amount', 'status', 'created_at', 'updated_at')

# admin.site.register(DebtPenalty):
