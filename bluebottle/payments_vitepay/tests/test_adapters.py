import json
import urllib

from moneyed.classes import Money, XOF, EUR
from mock import patch

from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from bluebottle.payments.exception import PaymentException
from bluebottle.payments_vitepay.adapters import VitepayPaymentAdapter
from bluebottle.test.factory_models.donations import DonationFactory
from bluebottle.test.factory_models.orders import OrderFactory
from bluebottle.test.factory_models.payments import OrderPaymentFactory
from bluebottle.test.factory_models.rates import RateSourceFactory, RateFactory

from bluebottle.test.utils import BluebottleTestCase

vitepay_settings = {
    'MERCHANT_ACCOUNTS': [
        {
            'merchant': 'vitepay',
            'currency': 'XOF',
            'api_key': '123',
            'api_secret': '123456789012345678901234567890123456789012345678901234567890',
            'api_url': 'https://api.vitepay.com/v1/prod/payments'
        }
    ]
}


@override_settings(**vitepay_settings)
class VitepayPaymentAdapterTestCase(BluebottleTestCase):
    @patch('bluebottle.payments_vitepay.adapters.get_current_host',
           return_value='https://onepercentclub.com')
    def test_create_payment(self, get_current_host):
        self.init_projects()
        order = OrderFactory.create()
        DonationFactory.create(amount=Money(2000, XOF), order=order)
        order_payment = OrderPaymentFactory.create(payment_method='vitepayOrangemoney', order=order)
        adapter = VitepayPaymentAdapter(order_payment)
        self.assertEqual(adapter.payment.amount_100, 200000)

    @patch('bluebottle.payments_vitepay.adapters.get_current_host',
           return_value='https://onepercentclub.com')
    def test_create_payment_with_wrong_currency(self, get_current_host):
        with self.assertRaises(PaymentException):
            order_payment = OrderPaymentFactory.create(payment_method='vitepayOrangemoney',
                                                       amount=Money(200, EUR))
            VitepayPaymentAdapter(order_payment)

    @patch('bluebottle.payments_vitepay.adapters.get_current_host',
           return_value='https://onepercentclub.com')
    def test_create_payment_with_wrong_payment_method(self, get_current_host):
        with self.assertRaises(PaymentException):
            order_payment = OrderPaymentFactory.create(payment_method='docdataIdeal',
                                                       amount=Money(3500, XOF))
            adapter = VitepayPaymentAdapter(order_payment)
            adapter.create_payment()


    @patch('bluebottle.payments_vitepay.adapters.get_current_host',
           return_value='https://onepercentclub.com')
    @patch('bluebottle.payments_vitepay.adapters.VitepayPaymentAdapter._create_payment_hash',
           return_value='123123')
    @patch('bluebottle.payments_vitepay.adapters.requests.post',
           return_value=type('obj', (object,), {'status_code': 200, 'content': 'https://vitepay.com/some-path-to-pay'}))
    def test_authorization_action(self, mock_post, get_current_host, create_hash):
        """
        Play some posts that Vitepay might fire at us.
        """
        self.init_projects()
        order = OrderFactory.create()
        DonationFactory.create(amount=Money(2000, XOF), order=order)
        order_payment = OrderPaymentFactory.create(payment_method='vitepayOrangemoney', order=order)
        adapter = VitepayPaymentAdapter(order_payment)
        authorization_action = adapter.get_authorization_action()
        data = {
            u"api_key": u"123",
            u"hash": u"123123",
            u"redirect": 0,
            u"payment": {
                u"description": u"Thanks for your donation!",
                u"order_id": u"opc-{}".format(order_payment.id),
                u"decline_url": u"https://onepercentclub.com/orders/{}/failed".format(order_payment.order.id),
                u"p_type": u"orange_money",
                u"country_code": u"ML",
                u"language_code": u"fr",
                u"amount_100": 200000,
                u"cancel_url": u"https://onepercentclub.com/orders/{}/failed".format(order_payment.order.id),
                u"currency_code": u"XOF",
                u"callback_url": u"https://onepercentclub.com/payments_vitepay/status_update/",
                u"return_url": u"https://onepercentclub.com/orders/{}/success".format(order_payment.order.id)
            }
        }

        self.assertEqual(mock_post.call_args[0][0], 'https://api.vitepay.com/v1/prod/payments')
        self.assertEqual(json.loads(mock_post.call_args[1]['data']), data)
        self.assertEqual(mock_post.call_args[1]['headers'], {'Content-Type': 'application/json'})

        self.assertEqual(authorization_action['url'], 'https://vitepay.com/some-path-to-pay')


    @patch('bluebottle.payments_vitepay.adapters.get_current_host',
           return_value='https://onepercentclub.com')
    def test_update_payment(self, get_current_host):
        """
        Play some posts that Vitepay might fire at us.
        """
        self.init_projects()
        order = OrderFactory.create()
        DonationFactory.create(amount=Money(2000, XOF), order=order)
        order_payment = OrderPaymentFactory.create(payment_method='vitepayOrangemoney', order=order)
        adapter = VitepayPaymentAdapter(order_payment)
        self.assertEqual(adapter.payment.amount_100, 200000)
        update_view = reverse('vitepay-status-update')
        authenticity = adapter._create_update_hash()
        data = {
            'success': 1,
            'order_id': adapter.payment.order_id,
            'authenticity': authenticity
        }
        response = self.client.post(update_view, data, format='multipart')
        self.assertEqual(response.content, '{"status": "1"}')
