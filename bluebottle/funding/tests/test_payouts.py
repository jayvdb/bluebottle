import mock

import bunch

import stripe

from django.urls import reverse
from django.contrib.auth.models import Group
from moneyed import Money

from bluebottle.funding.tests.factories import (
    FundingFactory, DonationFactory
)
from bluebottle.funding.models import Payout
from bluebottle.funding_flutterwave.models import FlutterwavePaymentProvider
from bluebottle.funding_flutterwave.tests.factories import FlutterwavePaymentProviderFactory, \
    FlutterwaveBankAccountFactory, FlutterwavePaymentFactory
from bluebottle.funding_lipisha.models import LipishaPaymentProvider
from bluebottle.funding_lipisha.tests.factories import LipishaPaymentProviderFactory, LipishaBankAccountFactory, \
    LipishaPaymentFactory
from bluebottle.funding_pledge.models import PledgePaymentProvider
from bluebottle.funding_stripe.models import (
    StripePayoutAccount, ExternalAccount
)
from bluebottle.funding_stripe.tests.factories import (
    ExternalAccountFactory,
    StripeSourcePaymentFactory
)
from bluebottle.funding_pledge.tests.factories import PledgePaymentFactory
from bluebottle.funding_vitepay.models import VitepayPaymentProvider
from bluebottle.funding_vitepay.tests.factories import (
    VitepayPaymentFactory, VitepayBankAccountFactory,
    VitepayPaymentProviderFactory
)
from bluebottle.funding_pledge.tests.factories import (
    PledgeBankAccountFactory, PledgePaymentProviderFactory
)
from bluebottle.initiatives.tests.factories import InitiativeFactory
from bluebottle.test.factory_models.accounts import BlueBottleUserFactory
from bluebottle.test.utils import (
    BluebottleTestCase, JSONAPITestClient
)


class BasePayoutTestCase(BluebottleTestCase):
    def setUp(self):
        super(BasePayoutTestCase, self).setUp()
        self.client = JSONAPITestClient()
        self.user = BlueBottleUserFactory()
        self.finance_user = BlueBottleUserFactory()
        self.finance_user.groups.add(Group.objects.get(name='Financial'))
        self.initiative = InitiativeFactory.create()

        self.initiative.transitions.submit()
        self.initiative.transitions.approve()
        self.initiative.save()


class StripePayoutTestCase(BasePayoutTestCase):
    def setUp(self):
        super(StripePayoutTestCase, self).setUp()
        self.funding = FundingFactory.create(
            owner=self.user,
            initiative=self.initiative,
            bank_account=ExternalAccountFactory.create()
        )
        with mock.patch.object(StripePayoutAccount, 'verified', return_value=True):
            self.funding.review_transitions.submit()
            self.funding.review_transitions.approve()
            self.funding.save()

        with mock.patch(
            'stripe.Source.modify'
        ):
            donation = DonationFactory.create(
                activity=self.funding,
                amount=Money(10, 'EUR'),
                status='succeeded',
            )
            StripeSourcePaymentFactory.create(donation=donation)

            donation = DonationFactory.create(
                activity=self.funding,
                amount=Money(100, 'USD'),
                status='succeeded',
            )
            StripeSourcePaymentFactory.create(donation=donation)

            donation = DonationFactory.create(
                activity=self.funding,
                amount=Money(10, 'USD'),
                status='failed',
            )
            StripeSourcePaymentFactory.create(donation=donation)

            donation = DonationFactory.create(
                activity=self.funding,
                amount=Money(10, 'EUR'),
            )
            PledgePaymentFactory.create(donation=donation)

    def test_payout(self):
        self.funding.transitions.succeed()

        dollar_payout = Payout.objects.get(currency='USD', provider='stripe')
        self.assertEqual(
            len(dollar_payout.donations.all()), 1
        )
        self.assertEqual(
            dollar_payout.total_amount, Money(100, 'USD')
        )

        euro_payout = Payout.objects.get(currency='EUR', provider='stripe')
        self.assertEqual(
            len(euro_payout.donations.all()), 1
        )
        self.assertEqual(
            euro_payout.total_amount, Money(10, 'EUR')
        )

        pledge_payout = Payout.objects.get(currency='EUR', provider='pledge')
        self.assertEqual(
            len(pledge_payout.donations.all()), 1
        )
        self.assertEqual(
            pledge_payout.total_amount, Money(10, 'EUR')
        )

    def test_payout_endpoint(self):
        self.funding.transitions.succeed()

        url = reverse('funding-payout-details', args=(self.funding.pk, ))

        stripe_bank_account = stripe.BankAccount('some-bank-token')
        stripe_bank_account.update(bunch.bunchify({
            'object': 'bank_account',
            'account_holder_name': 'Jane Austen',
            'account_holder_type': 'individual',
            'bank_name': 'STRIPE TEST BANK',
            'country': 'US',
            'currency': 'usd',
            'fingerprint': '1JWtPxqbdX5Gamtc',
            'last4': '6789',
            'metadata': {
                'order_id': '6735'
            },
            'routing_number': '110000000',
            'status': 'new',
            'account': 'acct_1032D82eZvKYlo2C'
        }))

        with mock.patch.object(ExternalAccount, 'account', new_callable=mock.PropertyMock) as mock_account:
            mock_account.return_value = stripe_bank_account
            response = self.client.get(
                url,
                user=self.finance_user
            )

        data = response.json()

        self.assertEqual(
            len(data['payouts']), 3
        )

        self.assertEqual(
            data['bank_account']['account_holder_name'], 'Jane Austen'
        )
        self.assertEqual(
            data['bank_account']['currency'], 'usd'
        )


class VitepayPayoutTestCase(BasePayoutTestCase):
    def setUp(self):
        super(VitepayPayoutTestCase, self).setUp()
        if not VitepayPaymentProvider.objects.count():
            VitepayPaymentProviderFactory.create()

        self.funding = FundingFactory.create(
            owner=self.user,
            initiative=self.initiative,
            bank_account=VitepayBankAccountFactory.create(
                reviewed=True,
                mobile_number='1234',
                account_name='Jane Austen'
            )
        )
        self.funding.review_transitions.submit()
        self.funding.review_transitions.approve()
        self.funding.save()
        donation = DonationFactory.create(
            activity=self.funding,
            amount=Money(10, 'XOF'),
            status='succeeded',
        )
        VitepayPaymentFactory.create(donation=donation)

        donation = DonationFactory.create(
            activity=self.funding,
            amount=Money(100, 'XOF'),
            status='failed',
        )
        VitepayPaymentFactory.create(donation=donation)

    def test_payout_endpoint(self):
        self.funding.transitions.succeed()

        url = reverse('funding-payout-details', args=(self.funding.pk, ))

        response = self.client.get(
            url,
            user=self.finance_user
        )

        data = response.json()

        self.assertEqual(
            len(data['payouts']), 1
        )

        self.assertEqual(
            data['bank_account'], {
                u'mobile_number': u'1234',
                u'type': u'vitepay',
                u'id': self.funding.bank_account.id,
                u'account_name': u'Jane Austen'
            }
        )


class LipishaPayoutTestCase(BasePayoutTestCase):
    def setUp(self):
        super(LipishaPayoutTestCase, self).setUp()
        if not LipishaPaymentProvider.objects.count():
            LipishaPaymentProviderFactory.create()

        self.funding = FundingFactory.create(
            owner=self.user,
            initiative=self.initiative,
            bank_account=LipishaBankAccountFactory.create(
                reviewed=True,
                account_number='1234',
                account_name='Jane Austen',
                mpesa_code='1212'
            )
        )
        self.funding.review_transitions.submit()
        self.funding.review_transitions.approve()
        self.funding.save()
        donation = DonationFactory.create(
            activity=self.funding,
            amount=Money(10000, 'KES'),
            status='succeeded',
        )
        LipishaPaymentFactory.create(donation=donation)

        donation = DonationFactory.create(
            activity=self.funding,
            amount=Money(10000, 'KES'),
            status='failed',
        )
        LipishaPaymentFactory.create(donation=donation)

    def test_payout_endpoint(self):
        self.funding.transitions.succeed()

        url = reverse('funding-payout-details', args=(self.funding.pk, ))

        response = self.client.get(
            url,
            user=self.finance_user
        )

        data = response.json()

        self.assertEqual(
            len(data['payouts']), 1
        )

        self.assertEqual(
            data['bank_account'], {
                u'bank_name': u'Big Duck Bank',
                u'bank_code': u'7337',
                u'account_name': u'Jane Austen',
                u'branch_name': u'Daffy',
                u'account_number': u'1234',
                u'address': u'Main street 1',
                u'branch_code': u'12',
                u'mpesa_code': u'1212',
                u'swift': u'12345',
                u'type': 'lipisha',
                u'id': self.funding.bank_account.id
            }
        )


class FlutterwavePayoutTestCase(BasePayoutTestCase):
    def setUp(self):
        super(FlutterwavePayoutTestCase, self).setUp()
        if not FlutterwavePaymentProvider.objects.count():
            FlutterwavePaymentProviderFactory.create()

        self.funding = FundingFactory.create(
            owner=self.user,
            initiative=self.initiative,
            bank_account=FlutterwaveBankAccountFactory.create(
                reviewed=True,
                account_number='1234',
                account='FW-0001'
            )
        )
        self.funding.review_transitions.submit()
        self.funding.review_transitions.approve()
        self.funding.save()
        donation = DonationFactory.create(
            activity=self.funding,
            amount=Money(10000, 'NGN'),
            status='succeeded',
        )
        FlutterwavePaymentFactory.create(donation=donation)

        donation = DonationFactory.create(
            activity=self.funding,
            amount=Money(10000, 'NGN'),
            status='failed',
        )
        FlutterwavePaymentFactory.create(donation=donation)

    def test_payout_endpoint(self):
        self.funding.transitions.succeed()

        url = reverse('funding-payout-details', args=(self.funding.pk, ))

        response = self.client.get(
            url,
            user=self.finance_user
        )

        data = response.json()

        self.assertEqual(
            len(data['payouts']), 1
        )

        self.assertEqual(
            data['bank_account'], {
                u'account_holder_name': u'Test Name',
                u'account_number': u'1234',
                u'bank_country_code': u'NG',
                u'account': u'FW-0001',
                u'bank_code': u'044',
                u'id': self.funding.bank_account.id
            }
        )


class PledgePayoutTestCase(BasePayoutTestCase):
    def setUp(self):
        super(PledgePayoutTestCase, self).setUp()
        if not PledgePaymentProvider.objects.count():
            PledgePaymentProviderFactory.create()

        self.funding = FundingFactory.create(
            owner=self.user,
            initiative=self.initiative,
            bank_account=PledgeBankAccountFactory.create(
                reviewed=True,
            )
        )
        self.funding.review_transitions.submit()
        self.funding.review_transitions.approve()
        self.funding.save()
        donation = DonationFactory.create(
            activity=self.funding,
            amount=Money(10, 'XOF'),
        )
        PledgePaymentFactory.create(donation=donation)

        donation = DonationFactory.create(
            activity=self.funding,
            amount=Money(100, 'XOF'),
        )
        payment = PledgePaymentFactory.create(donation=donation)
        payment.transitions.fail()

    def test_payout_endpoint(self):
        self.funding.transitions.succeed()

        url = reverse('funding-payout-details', args=(self.funding.pk, ))

        response = self.client.get(
            url,
            user=self.finance_user
        )

        data = response.json()

        self.assertEqual(
            len(data['payouts']), 1
        )

        self.assertEqual(
            data['bank_account']['account_holder_city'],
            self.funding.bank_account.account_holder_city
        )

        self.assertEqual(
            data['bank_account']['account_holder_country'],
            self.funding.bank_account.account_holder_country.code
        )
