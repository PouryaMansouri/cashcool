from django.apps import AppConfig


class CreditTransactionsConfig(AppConfig):
    name = 'credit_card.credit_transactions'

    def ready(self):
        import credit_card.credit_transactions.signals