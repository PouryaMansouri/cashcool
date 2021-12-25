from django.test import TestCase

from factory_boy.models import CreateOrganization, UserFactory, CreateCreditMarketer, CwalletRegularFactory, \
    CurrentCashtagFactory, CreateCreditCwalletFactory


class CreditCwalletTest(TestCase):
    def setUp(self):
        self.phone_number = "09132985527"

        self.user = UserFactory(phone_number=self.phone_number)
        self.cwallet = CwalletRegularFactory(user=self.user)
        self.oragn = CreateOrganization()
        self.credit_marketer = CreateCreditMarketer(marketer_cwallet=self.cwallet, organization=self.oragn)

        self.first_user = UserFactory()
        self.first_user_cwallet = CwalletRegularFactory(user=self.first_user)
        self.first_user_current_cashtag = CurrentCashtagFactory(cc_account=self.first_user_cwallet)
        self.first_user_cwallet.current_cashtag = self.first_user_current_cashtag

        self.first_user_current_credit_cashtag = CurrentCashtagFactory(cc_account=self.first_user_cwallet,
                                                                       cashtag=self.first_user_cwallet.current_cashtag.cashtag + '_credit')
        self.first_user_credit_card = CreateCreditCwalletFactory(cwallet=self.first_user_cwallet,
                                                                 credit_marketer=self.credit_marketer,
                                                                 current_cashtag=self.first_user_current_credit_cashtag)

        self.second_user = UserFactory()
        self.second_user_cwallet = CwalletRegularFactory(user=self.second_user)
        self.second_user_current_cashtag = CurrentCashtagFactory(cc_account=self.second_user_cwallet)
        self.second_user_cwallet.current_cashtag = self.second_user_current_cashtag
        self.second_user_current_credit_cashtag = CurrentCashtagFactory(cc_account=self.second_user_cwallet,
                                                                        cashtag=self.second_user_cwallet.current_cashtag.cashtag + '_credit')
        self.second_user_credit_card = CreateCreditCwalletFactory(cwallet=self.second_user_cwallet,
                                                                  credit_marketer=self.credit_marketer,
                                                                  current_cashtag=self.second_user_current_credit_cashtag,
                                                                  credit_amount=12000000, balance=12000000,
                                                                  checkout_period_month=2)

    def test_first_user_credit_cwallet(self):
        self.assertEqual(self.first_user_credit_card.credit_amount, 10000000)
        self.assertEqual(self.first_user_credit_card.balance, 10000000)
        self.assertEqual(self.first_user_credit_card.checkout_period_month, 1)
        self.assertEqual(self.first_user_credit_card.credit_marketer, self.credit_marketer)
        self.assertEqual(hasattr(self.first_user_credit_card, 'current_cashtag'), True)

    def test_second_user_credit_cwallet(self):
        self.assertEqual(self.second_user_credit_card.credit_amount, 12000000)
        self.assertEqual(self.second_user_credit_card.balance, 12000000)
        self.assertEqual(self.second_user_credit_card.checkout_period_month, 2)
        self.assertEqual(self.second_user_credit_card.credit_marketer, self.credit_marketer)
        self.assertEqual(hasattr(self.second_user_credit_card, 'current_cashtag'), True)
