import os
from mock import patch

from bluebottle.utils.utils import json2obj
from django.contrib.admin import AdminSite

from bluebottle.payouts.models import StripePayoutAccount
from django.contrib.auth.models import Permission, Group
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from bluebottle.test.factory_models.accounts import BlueBottleUserFactory
from bluebottle.test.factory_models.payouts import PlainPayoutAccountFactory, StripePayoutAccountFactory
from bluebottle.test.utils import BluebottleAdminTestCase
from bluebottle.payouts.admin.stripe import StripePayoutAccountAdmin

from ..admin import ProjectPayoutAdmin


MERCHANT_ACCOUNTS = [
    {
        'merchant': 'stripe',
        'currency': 'EUR',
        'secret_key': 'sk_test_secret_key',
        'webhook_secret': 'whsec_test_webhook_secret',
        'webhook_secret_connect': 'whsec_test_webhook_secret_connect',
    }
]

PROJECT_PAYOUT_FEES = {
    'beneath_threshold': 1,
    'fully_funded': 0.05,
    'not_fully_funded': 0.0725
}


@override_settings(MERCHANT_ACCOUNTS=MERCHANT_ACCOUNTS)
class StripePayoutTestAdmin(BluebottleAdminTestCase):
    def setUp(self):
        super(StripePayoutTestAdmin, self).setUp()
        self.payout = StripePayoutAccountFactory.create(

        )
        self.site = AdminSite()
        self.admin = StripePayoutAccountAdmin(StripePayoutAccount, self.site)

    @patch('bluebottle.payouts.models.stripe.Account.retrieve')
    def test_stripe_details(self, stripe_retrieve):
        stripe_retrieve.return_value = json2obj(
            open(os.path.dirname(__file__) + '/data/stripe_account_verified.json').read()
        )
        details = self.admin.details(self.payout)
        self.assertEqual(details,
                         '<b>account number</b>: *************1234<br/>'
                         '<b>account holder name</b>: Malle Eppie<br/>'
                         '<b>last name</b>: Eppie<br/>'
                         '<b>country</b>: NL<br/>'
                         '<b>bank country</b>: DE<br/><b>currency</b>: eur<br/>'
                         '<b>first name</b>: Malle')


class PayoutTestAdmin(BluebottleAdminTestCase):
    """ verify expected fields/behaviour is present """

    def test_extra_listfields(self):
        self.failUnless('amount_pending' in ProjectPayoutAdmin.list_display)
        self.failUnless('amount_raised' in ProjectPayoutAdmin.list_display)

    @override_settings(PROJECT_PAYOUT_FEES=PROJECT_PAYOUT_FEES)
    def test_decimal_payout_rules(self):
        # Check payout rules show decimal (if there are any)
        payout_url = reverse('admin:payouts_projectpayout_changelist')
        response = self.app.get(payout_url, user=self.superuser)
        self.failUnless('5%' in response.body)
        self.failUnless('7.25%' in response.body)


class PayoutAccountAdminTestCase(BluebottleAdminTestCase):

    def setUp(self):
        self.user = BlueBottleUserFactory.create(is_staff=True)
        account = PlainPayoutAccountFactory.create()
        self.payout_url = reverse('admin:payouts_payoutaccount_change', args=(account.id,))

    def test_permissions_denied(self):
        self.client.force_login(self.user)
        response = self.client.get(self.payout_url)
        self.assertEqual(response.status_code, 403)

    def test_permissions_granted_user(self):
        # Check user has permission when added specific permission
        self.user.user_permissions.add(
            Permission.objects.get(codename='change_plainpayoutaccount')
        )
        self.client.force_login(self.user)
        response = self.client.get(self.payout_url)
        self.assertEqual(response.status_code, 200)

    def test_permissions_granted_staff(self):
        # Check that user has permission if added to Staff group
        self.user.groups.add(Group.objects.get(name='Staff'))
        self.client.force_login(self.user)
        response = self.client.get(self.payout_url)
        self.assertEqual(response.status_code, 200)
