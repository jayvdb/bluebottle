import mock
from decimal import Decimal

from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from rest_framework import status

from bluebottle.clients import properties
from bluebottle.test.utils import BluebottleTestCase
from bluebottle.test.factory_models.accounts import BlueBottleUserFactory


class ClientSettingsTestCase(BluebottleTestCase):

    def setUp(self):
        super(ClientSettingsTestCase, self).setUp()
        self.settings_url = reverse('settings')

    @override_settings(CLOSED_SITE=False, TOP_SECRET="*****", EXPOSED_TENANT_PROPERTIES=['closed_site'])
    def test_settings_show(self):
        # Check that exposed property is in settings api, and other settings are not shown
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['closedSite'], False)
        self.assertNotIn('topSecret', response.data)

        # Check that exposed setting gets overwritten by client property
        setattr(properties, 'CLOSED_SITE', True)
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['closedSite'], True)

        # Check that previously hidden setting can be exposed
        setattr(properties, 'EXPOSED_TENANT_PROPERTIES', ['closed_site', 'top_secret'])
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('topSecret', response.data)

        setattr(properties, 'CLOSED_SITE', False)

    @override_settings(TOKEN_AUTH={'assertion_mapping': {'first_name': 'urn:first_name'}})
    def test_settings_read_only(self):
        # Check that exposed property is in settings api, and other settings are not shown
        response = self.client.get(self.settings_url)
        self.assertEqual(response.data['readOnlyFields'], {'user': ['first_name']})

    @override_settings(PAYMENT_METHODS=[{
        'provider': 'docdata',
        'id': 'docdata-ideal',
        'profile': 'ideal',
        'name': 'iDEAL',
        'restricted_countries': ('NL', ),
        'supports_recurring': False,
        'currencies': {
            'EUR': {'min_amount': 5, 'max_amount': 100}
        }
    }, {
        'provider': 'docdata',
        'id': 'docdata-directdebit',
        'profile': 'directdebit',
        'name': 'Direct Debit',
        'restricted_countries': ('NL', 'BE', ),
        'supports_recurring': True,
        'currencies': {
            'EUR': {'min_amount': 10, 'max_amount': 100}
        }

    }, {
        'provider': 'docdata',
        'id': 'docdata-creditcard',
        'profile': 'creditcard',
        'name': 'CreditCard',
        'supports_recurring': False,
        'currencies': {
            'USD': {'min_amount': 5, 'max_amount': 100},
            'NGN': {'min_amount': 3000, 'max_amount': 100},
            'XOF': {'min_amount': 5000, 'max_amount': 100},
        }
    }])
    def test_settings_currencies(self):
        # Check that exposed property is in settings api, and other settings are not shown
        response = self.client.get(self.settings_url)

        self.assertEqual(
            response.data['currencies'],
            [
                {
                    'symbol': u'CFA',
                    'code': 'XOF',
                    'name': u'West African CFA Franc',
                    'rate': Decimal(1000.0),
                    'minAmount': 5000
                },
                {
                    'symbol': u'\u20a6',
                    'code': 'NGN',
                    'name': u'Nigerian Naira',
                    'rate': Decimal(500.0),
                    'minAmount': 3000
                },
                {
                    'symbol': u'$',
                    'code': 'USD',
                    'name': u'US Dollar',
                    'rate': Decimal(1.0),
                    'minAmount': 5
                },
                {
                    'symbol': u'\u20ac',
                    'code': 'EUR',
                    'name': u'Euro',
                    'rate': Decimal(1.5),
                    'minAmount': 5
                }
            ]
        )


class TestDefaultAPI(BluebottleTestCase):
    """
        Test the default API, open and closed, authenticated or not
        with default permissions
    """
    def setUp(self):
        super(TestDefaultAPI, self).setUp()

        self.init_projects()
        self.user = BlueBottleUserFactory.create()
        self.user_token = "JWT {0}".format(self.user.get_jwt_token())
        self.projects_url = reverse('project_list')

    def test_open_api(self):
        """ request open api, expect projects """
        response = self.client.get(self.projects_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @mock.patch('bluebottle.clients.properties.CLOSED_SITE', True)
    def test_closed_api_not_authenticated(self):
        """ request closed api, expect 403 ? if not authenticated """
        response = self.client.get(self.projects_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch('bluebottle.clients.properties.CLOSED_SITE', True)
    def test_closed_api_authenticated(self):
        """ request closed api, expect projects if authenticated """
        response = self.client.get(self.projects_url, token=self.user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
