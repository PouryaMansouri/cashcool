from credit_card.credit_cwallets.models import CreditCwallet
from cwallets.models import CWalletRegular


# TODO update credit cwallet for amount
def create_credit_cwallet_from_another_app(cwallet: CWalletRegular, credit_marketer, credit_amount,checkout_period_month):
    credit_cwallet = CreditCwallet.objects.filter(cwallet=cwallet, credit_marketer=credit_marketer)

    if not credit_cwallet:
        credit_cwallet = CreditCwallet.objects.create(cwallet=cwallet, credit_marketer=credit_marketer,
                                                      credit_amount=credit_amount, balance =credit_amount, checkout_period_month=checkout_period_month)

    return credit_cwallet
