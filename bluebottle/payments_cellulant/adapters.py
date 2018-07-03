# coding=utf-8
import logging

from mula.adpaters import MulaAdapter

from bluebottle.payments.adapters import BasePaymentAdapter
from bluebottle.utils.utils import StatusDefinition

from .models import CellulantPayment

logger = logging.getLogger()


class CellulantPaymentAdapter(BasePaymentAdapter):
    card_data = {}

    STATUS_MAPPING = {
        'Requested': StatusDefinition.CREATED,
        'Completed': StatusDefinition.SETTLED,
        'Cancelled': StatusDefinition.CANCELLED,
        'Voided': StatusDefinition.FAILED,
        'Acknowledged': StatusDefinition.AUTHORIZED,
        'Authorized': StatusDefinition.AUTHORIZED,
        'Settled': StatusDefinition.SETTLED,
        'Reversed': StatusDefinition.REFUNDED
    }

    def __init__(self, order_payment):
        self.order_payment = order_payment
        self.client = MulaAdapter(
            self.credentials['client_id'],
            self.credentials['client_secret'],
            self.credentials['client_code']
        )
        super(CellulantPaymentAdapter, self).__init__(order_payment)

    def _get_mapped_status(self, status):
        return self.STATUS_MAPPING[status]

    def create_payment(self):
        payment = CellulantPayment(
            order_payment=self.order_payment,
        )
        payment.msisdn = '254800000000'
        payment.account_number = '123456'
        payment.reference = payment.order_payment.id
        payment.amount = payment.order_payment.amount.amount

        response = self.client.initiate_transaction(
            msisdn=payment.msisdn,
            transaction_reference_id=payment.reference,
            account_number=payment.account_number,
            amount=payment.amount,
            currency_code='KES',
            country_code='KE',
            payment_method='MPESA',
            language='en',
            payment_option='Mobile Money',
            payment_mode='push notification',
            callback_url=''
        )
        if response['results']:
            payment.remote_reference = response['results']['reference']
            payment.save()
        if response['status']['statusCode'] == 500:
            payment.status = 'failed'
            payment.save()
        return payment

    def get_authorization_action(self):

        if self.payment.status == 'started':
            return {
                'type': 'process',
                'payload': {
                    'business_number': self.credentials['business_number'],
                    'account_number': self.order_payment.order.project,
                    'amount': int(float(self.order_payment.amount))
                }
            }
        else:
            self.check_payment_status()
            if self.payment.status in ['settled', 'authorized']:
                return {
                    'type': 'success'
                }
            else:
                return {
                    'type': 'pending'
                }

    def check_payment_status(self):
        pass
