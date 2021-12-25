from django.apps import AppConfig


class DebtCreditCwalletsConfig(AppConfig):
    name = 'credit_card.debts'

    def ready(self):
        import credit_card.debts.signals