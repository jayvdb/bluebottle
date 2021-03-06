from rest_framework import serializers

from rest_framework_json_api.relations import ResourceRelatedField

from bluebottle.funding.base_serializers import PaymentSerializer, BaseBankAccountSerializer
from bluebottle.funding_pledge.models import PledgePayment, PledgeBankAccount
from bluebottle.geo.models import Country


class PledgePaymentSerializer(PaymentSerializer):
    class Meta(PaymentSerializer.Meta):
        model = PledgePayment

    class JSONAPIMeta(PaymentSerializer.JSONAPIMeta):
        resource_name = 'payments/pledge-payments'


class PledgeBankAccountSerializer(BaseBankAccountSerializer):
    account_holder_country = ResourceRelatedField(queryset=Country.objects, required=False)
    account_bank_country = ResourceRelatedField(queryset=Country.objects, required=False)

    class Meta(BaseBankAccountSerializer.Meta):
        model = PledgeBankAccount

        fields = BaseBankAccountSerializer.Meta.fields + (
            'account_holder_name',
            'account_holder_address',
            'account_holder_postal_code',
            'account_holder_city',
            'account_number',
            'account_details',

            'account_holder_country',
            'account_bank_country'
        )

    included_serializers = {
        'account_holder_country': 'bluebottle.geo.serializers.InitiativeCountrySerializer',
        'account_bank_country': 'bluebottle.geo.serializers.InitiativeCountrySerializer',
        'connect_account': 'bluebottle.funding.serializers.PlainPayoutAccountSerializer',
    }

    class JSONAPIMeta(BaseBankAccountSerializer.JSONAPIMeta):
        resource_name = 'payout-accounts/pledge-external-accounts'


class PayoutPledgeBankAccountSerializer(serializers.ModelSerializer):
    account_holder_country = serializers.CharField(read_only=True, source='account_holder_country.code')
    account_bank_country = serializers.CharField(read_only=True, source='account_bank_country.code')

    class Meta(BaseBankAccountSerializer.Meta):
        model = PledgeBankAccount

        fields = (
            'id',
            'account_holder_name',
            'account_holder_address',
            'account_holder_postal_code',
            'account_holder_city',
            'account_number',
            'account_details',

            'account_holder_country',
            'account_bank_country'
        )
