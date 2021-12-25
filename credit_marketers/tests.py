from django.test import TestCase

from factory_boy.models import CreateOrganization, UserFactory, CreateCreditMarketer, CwalletRegularFactory


class MarketerTest(TestCase):
    def setUp(self):
        self.phone_number = "09132985527"

        self.user = UserFactory(phone_number=self.phone_number)
        self.cwallet = CwalletRegularFactory(user=self.user)
        self.oragn = CreateOrganization()
        self.credit_marketer = CreateCreditMarketer(marketer_cwallet=self.cwallet, organization=self.oragn)

    def test_credit_marketer(self):
        self.assertEqual(self.credit_marketer.transaction_amount_remain, 1000000000)
        self.assertEqual(self.oragn.name, "Edare Gaz")
        self.assertEqual(self.credit_marketer.organization.name, "Edare Gaz")
        self.assertEqual(hasattr(self.credit_marketer.organization, 'nickname'), True)



    #TODO: test remain credit for marketer
