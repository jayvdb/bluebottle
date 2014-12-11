from bluebottle.terms.models import Terms, TermsAgreement
from rest_framework import serializers


class TermsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Terms
        fields = ('id', 'date', 'version', 'contents')
        
        
class TermsAgreementSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TermsAgreement
        fields = ('id', 'terms', 'user')
