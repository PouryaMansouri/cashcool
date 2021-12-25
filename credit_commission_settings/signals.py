from django.db import transaction as db_transaction
from django.db.models import Sum

from .constans import COMMISSION_TYPE_CHOICES
from .models import CreditCommissionSetting
from ..credit_transactions.models import CreditTransaction
from ..credit_transactions.serializers import CreditTransactionCreateSerializer
from ..credit_transactions.signals import post_atomic_credit_transaction


def create_commission_transaction_after_credit_transaction(sender, instance, **kwargs):
    receivers = CreditCommissionSetting.objects.filter(
        credit_marketer=instance.sender.credit_marketer, club=instance.receiver,
        type=COMMISSION_TYPE_CHOICES.percentage)
    if receivers:
        # TODO get with query
        cashcool_credit_id = 2

        with db_transaction.atomic():
            # first transaction to CashCool
            quantity_sum = receivers.aggregate(Sum('quantity'))
            quantity_sum = quantity_sum['quantity__sum']
            amount_in_rial = (quantity_sum * instance.amount) / 100
            amount_in_rial = round(amount_in_rial, 0)
            # TODO automate create of credit cwallet for cashcool
            data = {
                "sender": instance.receiver.id,
                "receiver": cashcool_credit_id,
                "amount": amount_in_rial,
                "commission_transaction": True,
                "commission_transaction_parent": instance.id,
                "send_debt": False,
                "send_signal": False,
                "pay_from_demand":True
            }
            base_commission_transaction = CreditTransactionCreateSerializer(data=data)
            if base_commission_transaction.is_valid():
                base_commission_transaction.save()

            receivers_exclude_cashcool = receivers.exclude(receiver_id=cashcool_credit_id)
            # other transactions to from cashcool to all others
            for i in receivers_exclude_cashcool:
                amount_in_rial = (i.quantity * instance.amount) / 100
                amount_in_rial = round(amount_in_rial, 0)
                data = {
                    "sender": cashcool_credit_id,
                    "receiver": i.receiver.id,
                    "amount": amount_in_rial,
                    "commission_transaction": True,
                    "commission_transaction_parent": instance.id,
                    "send_debt": False,
                    "send_signal": False,
                    "pay_from_demand": True
                }
                base_commission_transaction = CreditTransactionCreateSerializer(data=data)
                if base_commission_transaction.is_valid():
                    base_commission_transaction.save()


post_atomic_credit_transaction.connect(create_commission_transaction_after_credit_transaction, sender=CreditTransaction)




