import json

from django.core.urlresolvers import reverse

from rest_framework import status

from bluebottle.bb_projects.models import ProjectPhase
from bluebottle.projects.models import PartnerOrganization
from bluebottle.test.factory_models.categories import CategoryFactory
from bluebottle.test.utils import BluebottleTestCase
from bluebottle.test.factory_models.projects import ProjectFactory
from bluebottle.test.factory_models.organizations import OrganizationFactory


class CategoriesTestCase(BluebottleTestCase):
    """
    Integration tests for the Categories API.
    """

    def setUp(self):
        super(CategoriesTestCase, self).setUp()
        self.init_projects()

    def test_partner_project(self):
        cat = {
            'title_en': 'Nice things',
            'title_nl': 'Leuke dingen',
            'description_nl': 'Tralala bla bla',
            'description_en': 'Chit chat blah blah'
        }

        CategoryFactory.create(**cat)

        url = reverse('category-list')

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]['title'], cat['title_en'])

        # Confirm that we can restrieve dutch titles too.
        response = self.client.get(url, {'language': 'nl'})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]['title'], cat['title_nl'])


