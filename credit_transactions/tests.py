from django.test import TestCase
from django.urls import reverse

from credit_card.credit_cwallets.constants import CREDIT_CWALLET_CHOICES
from factory_boy.models import CreateOrganization, UserFactory, CreateCreditMarketer, CwalletRegularFactory, \
    CreateCreditCwalletFactory, CurrentCashtagFactory, DemandSettingFactory


class CreditTransactionTest(TestCase):
    def setUp(self):
        '''First Marketer'''
        self.phone_number = "09132985527"
        self.user = UserFactory(phone_number=self.phone_number)
        self.cwallet = CwalletRegularFactory(user=self.user)
        self.oragn = CreateOrganization()
        self.credit_marketer = CreateCreditMarketer(marketer_cwallet=self.cwallet, organization=self.oragn)

        '''Second Marketer'''
        self.phone_number2 = "09140141212"
        self.user2 = UserFactory(phone_number=self.phone_number2)
        self.cwallet2 = CwalletRegularFactory(user=self.user2)
        self.oragn2 = CreateOrganization(name="فرمانداری", nickname="farmandari")
        self.credit_marketer2 = CreateCreditMarketer(marketer_cwallet=self.cwallet2, organization=self.oragn2)

        '''First User'''
        self.first_user = UserFactory()
        self.first_user_cwallet = CwalletRegularFactory(user=self.first_user)
        self.first_user_current_cashtag = CurrentCashtagFactory(cc_account=self.first_user_cwallet)
        self.first_user_cwallet.current_cashtag = self.first_user_current_cashtag

        self.first_user_current_credit_cashtag = CurrentCashtagFactory(cc_account=self.first_user_cwallet,
                                                                       cashtag=self.first_user_cwallet.current_cashtag.cashtag + '_credit')
        self.first_user_credit_card = CreateCreditCwalletFactory(cwallet=self.first_user_cwallet,
                                                                 credit_marketer=self.credit_marketer,
                                                                 current_cashtag=self.first_user_current_credit_cashtag)
        '''Second User'''
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

        '''Third User'''
        self.third_user = UserFactory()
        self.third_user_cwallet = CwalletRegularFactory(user=self.third_user)
        self.third_user_current_cashtag = CurrentCashtagFactory(cc_account=self.third_user_cwallet)
        self.third_user_cwallet.current_cashtag = self.third_user_current_cashtag
        self.third_user_current_credit_cashtag = CurrentCashtagFactory(cc_account=self.third_user_cwallet,
                                                                       cashtag=self.third_user_cwallet.current_cashtag.cashtag + '_credit')
        self.third_user_credit_card = CreateCreditCwalletFactory(cwallet=self.third_user_cwallet,
                                                                 credit_marketer=self.credit_marketer,
                                                                 current_cashtag=self.third_user_current_credit_cashtag,
                                                                 credit_amount=12000000, balance=12000000,
                                                                 checkout_period_month=2,
                                                                 status=CREDIT_CWALLET_CHOICES.banned)

        self.club = UserFactory()
        self.club_cwallet = CwalletRegularFactory(user=self.club)
        self.club_current_cashtag = CurrentCashtagFactory(cc_account=self.club_cwallet)
        self.club_cwallet.current_cashtag = self.club_current_cashtag
        self.club_current_credit_cashtag = CurrentCashtagFactory(cc_account=self.club_cwallet,
                                                                 cashtag=self.club_cwallet.current_cashtag.cashtag + '_credit')
        self.club_demand_setting = DemandSettingFactory()
        self.club_credit_card = CreateCreditCwalletFactory(cwallet=self.club_cwallet,
                                                           credit_marketer=self.credit_marketer,
                                                           current_cashtag=self.club_current_credit_cashtag,
                                                           credit_amount=12000000, balance=12000000,
                                                           checkout_period_month=2, is_demand=True,
                                                           demand_setting=self.club_demand_setting)

        '''Second Club'''
        self.club2 = UserFactory()
        self.club2_cwallet = CwalletRegularFactory(user=self.club2)
        self.club2_current_cashtag = CurrentCashtagFactory(cc_account=self.club2_cwallet)
        self.club2_cwallet.current_cashtag = self.club2_current_cashtag
        self.club2_current_credit_cashtag = CurrentCashtagFactory(cc_account=self.club2_cwallet,
                                                                  cashtag=self.club2_cwallet.current_cashtag.cashtag + '_credit')
        self.club2_demand_setting = DemandSettingFactory()
        self.club2_credit_card = CreateCreditCwalletFactory(cwallet=self.club2_cwallet,
                                                            credit_marketer=self.credit_marketer2,
                                                            current_cashtag=self.club2_current_credit_cashtag,
                                                            credit_amount=12000000, balance=12000000,
                                                            checkout_period_month=2, is_demand=True,
                                                            demand_setting=self.club2_demand_setting)
        3

        '''third Club'''
        self.club3 = UserFactory()
        self.club3_cwallet = CwalletRegularFactory(user=self.club3)
        self.club3_current_cashtag = CurrentCashtagFactory(cc_account=self.club3_cwallet)
        self.club3_cwallet.current_cashtag = self.club3_current_cashtag
        self.club3_current_credit_cashtag = CurrentCashtagFactory(cc_account=self.club3_cwallet,
                                                                  cashtag=self.club3_cwallet.current_cashtag.cashtag + '_credit')
        self.club3_demand_setting = DemandSettingFactory()
        self.club3_credit_card = CreateCreditCwalletFactory(cwallet=self.club3_cwallet,
                                                            credit_marketer=self.credit_marketer,
                                                            current_cashtag=self.club3_current_credit_cashtag,
                                                            credit_amount=12000000, balance=12000000,
                                                            checkout_period_month=2, is_demand=True,
                                                            demand_setting=self.club3_demand_setting,
                                                            status=CREDIT_CWALLET_CHOICES.banned)

    def test_failed_sender_is_banned(self):
        '''
         Sender Credit Cwallet shouldn't be banned
        '''
        body = {
            "sender": self.third_user_credit_card.id,
            "receiver": self.club_credit_card.id,
            "amount": 15000
        }
        tx_result = self.client.post(reverse("credit_transactions:transaction"), body, format='json',
                                     content_type="application/json")

        self.assertEqual(tx_result.status_code, 400)
        self.assertEqual(str(tx_result.data['message']), "Sender Is Banned.")
        self.assertEqual(tx_result.data['message'].code, 'error')

    def test_failed_club_is_banned(self):
        '''
         Club Credit Cwallet shouldn't be banned
        '''
        body = {
            "sender": self.first_user_credit_card.id,
            "receiver": self.club3_credit_card.id,
            "amount": 15000
        }
        tx_result = self.client.post(reverse("credit_transactions:transaction"), body, format='json',
                                     content_type="application/json")

        self.assertEqual(tx_result.status_code, 400)
        self.assertEqual(str(tx_result.data['message']), "Club Is Banned.")
        self.assertEqual(tx_result.data['message'].code, 'error')



    def test_failed_to_non_club_transaction(self):
        '''
        receiver credit card should has 'is_demand' attr and it has to be True. but it's not!
        '''
        body = {
            "sender": self.first_user_credit_card.id,
            "receiver": self.second_user_credit_card.id,
            "amount": 15000
        }
        # TODO add authiorizaiton after adding in real code
        tx_result = self.client.post(reverse("credit_transactions:transaction"), body, format='json',
                                     content_type="application/json")

        self.assertEqual(tx_result.status_code, 400)
        self.assertEqual(str(tx_result.data['message']), 'Receiver should be club.')
        self.assertEqual(tx_result.data['message'].code, 'error')

    def test_failed_with_not_enough_balance_transaction(self):
        '''
        first user has only 10,0000,000 rial credit.
        it doesn't matter if receiver is not a club.
        '''
        body = {
            "sender": self.first_user_credit_card.id,
            "receiver": self.club_credit_card.id,
            "amount": 15000000
        }
        # TODO add authiorizaiton after adding in real code
        tx_result = self.client.post(reverse("credit_transactions:transaction"), body, format='json',
                                     content_type="application/json")

        self.assertEqual(tx_result.status_code, 400)
        self.assertEqual(str(tx_result.data['message']), 'not enough balance.')
        self.assertEqual(tx_result.data['message'].code, 'error')

    def test_failed_with_amount_lower_than_1000_transaction(self):
        '''
        first user has only 10,0000,000 rial credit.
        it doesn't matter if receiver is not a club.
        '''
        body = {
            "sender": self.first_user_credit_card.id,
            "receiver": self.club_credit_card.id,
            "amount": 10
        }
        # TODO add authiorizaiton after adding in real code
        tx_result = self.client.post(reverse("credit_transactions:transaction"), body, format='json',
                                     content_type="application/json")

        self.assertEqual(tx_result.status_code, 400)
        self.assertEqual(str(tx_result.data['message']), 'Transaction amount should be more than 1000.')
        self.assertEqual(tx_result.data['message'].code, 'error')

    def test_failed_with_diffrent_marketer(self):
        '''
        Both User and Club should have the same Marketer
        '''
        body = {
            "sender": self.first_user_credit_card.id,
            "receiver": self.club2_credit_card.id,
            "amount": 10
        }
        # TODO add authiorizaiton after adding in real code
        tx_result = self.client.post(reverse("credit_transactions:transaction"), body, format='json',
                                     content_type="application/json")

        self.assertEqual(tx_result.status_code, 400)
        self.assertEqual(str(tx_result.data['message']), 'Not Compatible Marketer Organization.')
        self.assertEqual(tx_result.data['message'].code, 'error')

    def test_correct_transaction(self):
        '''
        correct transaction
        '''
        body = {
            "sender": self.first_user_credit_card.id,
            "receiver": self.club_credit_card.id,
            "amount": 15001,
        }
        # TODO add authiorizaiton after adding in real code
        tx_result = self.client.post(reverse("credit_transactions:transaction"), body, format='json',
                                     content_type="application/json")

        correct_result = {'sender': self.first_user_credit_card.id, 'receiver': self.club_credit_card.id,
                          'amount': '15001', 'commission_transaction': False,
                          'commission_transaction_parent': None, 'send_signal': True, 'send_debt': True,
                          'pay_from_demand': False}
        self.assertEqual(tx_result.status_code, 201)
        self.assertEqual(tx_result.data, correct_result)

    def test_failed_with_repetitive_transaction(self):
        '''
           repetitive_transaction under 30s
        '''
        body = {
            "sender": self.first_user_credit_card.id,
            "receiver": self.club_credit_card.id,
            "amount": 15001,
        }
        # TODO add authiorizaiton after adding in real code
        first_tx_result = self.client.post(reverse("credit_transactions:transaction"), body, format='json',
                                           content_type="application/json")
        second_tx_result = self.client.post(reverse("credit_transactions:transaction"), body, format='json',
                                            content_type="application/json")
        first_result = {'sender': self.first_user_credit_card.id, 'receiver': self.club_credit_card.id,
                        'amount': '15001', 'commission_transaction': False,
                        'commission_transaction_parent': None, 'send_signal': True, 'send_debt': True,
                        'pay_from_demand': False}

        '''fist transaction should be correct'''
        self.assertEqual(first_tx_result.status_code, 201)
        self.assertEqual(first_tx_result.data, first_result)

        self.assertEqual(second_tx_result.status_code, 400)
        self.assertEqual(str(second_tx_result.data['message']), 'Repetitive Transaction Detected.')
        self.assertEqual(second_tx_result.data['message'].code, 'error')
