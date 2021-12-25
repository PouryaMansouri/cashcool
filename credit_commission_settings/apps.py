from django.apps import AppConfig


class CreditCommissionSettingsConfig(AppConfig):
    name = 'credit_card.credit_commission_settings'

    def ready(self):
        import credit_card.credit_commission_settings.signals