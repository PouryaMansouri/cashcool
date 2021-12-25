from .models import Debt, DebtHistory
from ..credit_transactions.models import CreditTransaction
from ..credit_transactions.signals import post_atomic_credit_transaction_for_debt_creation


def CreateDebtCreditCwalletAfterCreditTransaction(sender, instance, **kwargs):
    debt_credit_cwallet = Debt.objects.create(
        credit_cwallet=instance.sender, credit_transaction=instance
    )

    debt_history = DebtHistory.objects.create(debt_credit_cwallet=debt_credit_cwallet,
                                              amount=-(instance.amount))

    return debt_credit_cwallet


post_atomic_credit_transaction_for_debt_creation.connect(CreateDebtCreditCwalletAfterCreditTransaction,
                                                         sender=CreditTransaction)
