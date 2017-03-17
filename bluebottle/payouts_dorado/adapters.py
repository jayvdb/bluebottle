import requests
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from requests.exceptions import MissingSchema

from bluebottle.clients import properties
from bluebottle.payouts_dorado.exceptions import PayoutException


class DoradoPayoutAdapter(object):

    def __init__(self, project):
        self.settings = getattr(properties, 'PAYOUT_SERVICE', None)
        self.project = project
        self.tenant = connection.tenant

    def trigger_payout(self):
        # Send the signal to Dorado
        data = {
            'project_id': self.project.id,
            'tenant': self.tenant.schema_name
        }

        try:
            response = requests.post(self.settings['url'], data)
            if response.content != '{"status": "success"}':
                raise PayoutException(response.content)

            self.project.payout_status = 'created'
            self.project.save()
        except MissingSchema:
            raise ImproperlyConfigured("Incorrect Payout URL")
        except TypeError:
            raise ImproperlyConfigured("Invalid Payout settings")
