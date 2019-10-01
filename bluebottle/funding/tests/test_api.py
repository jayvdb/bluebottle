import json
from datetime import timedelta
import mock

import stripe

from django.urls import reverse
from django.utils.timezone import now
from moneyed import Money
from rest_framework import status

from bluebottle.funding.tests.factories import FundingFactory, FundraiserFactory, RewardFactory, DonationFactory
from bluebottle.funding.models import Donation
from bluebottle.funding.transitions import DonationTransitions
from bluebottle.funding_flutterwave.tests.factories import FlutterwavePaymentProviderFactory
from bluebottle.funding_stripe.tests.factories import ExternalAccountFactory, StripePaymentProviderFactory
from bluebottle.initiatives.tests.factories import InitiativeFactory
from bluebottle.test.factory_models.accounts import BlueBottleUserFactory
from bluebottle.test.factory_models.geo import GeolocationFactory
from bluebottle.test.utils import BluebottleTestCase, JSONAPITestClient, get_included


class BudgetLineListTestCase(BluebottleTestCase):
    def setUp(self):
        super(BudgetLineListTestCase, self).setUp()
        self.client = JSONAPITestClient()
        self.user = BlueBottleUserFactory()
        self.initiative = InitiativeFactory.create()

        self.initiative.transitions.submit()
        self.initiative.transitions.approve()

        self.funding = FundingFactory.create(
            owner=self.user,
            initiative=self.initiative,
        )

        self.create_url = reverse('funding-budget-line-list')
        self.funding_url = reverse('funding-detail', args=(self.funding.pk, ))

        self.data = {
            'data': {
                'type': 'activities/budget-lines',
                'attributes': {
                    'description': 'test',
                    'amount': {'amount': 100, 'currency': 'EUR'},
                },
                'relationships': {
                    'activity': {
                        'data': {
                            'type': 'activities/fundings',
                            'id': self.funding.pk,
                        }
                    }
                }
            }
        }

    def test_create(self):
        response = self.client.post(self.create_url, data=json.dumps(self.data), user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)

        self.assertEqual(
            data['data']['attributes']['description'],
            self.data['data']['attributes']['description']
        )

        response = self.client.get(self.funding_url, user=self.user)
        funding_data = json.loads(response.content)

        self.assertEqual(
            len(funding_data['data']['relationships']['budget-lines']['data']), 1
        )
        self.assertEqual(
            funding_data['data']['relationships']['budget-lines']['data'][0]['id'],
            data['data']['id']
        )

    def test_create_wrong_currency(self):
        self.data['data']['attributes']['amount']['currency'] = 'USD'
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.data),
            user=BlueBottleUserFactory.create()
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_other_user(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.data),
            user=BlueBottleUserFactory.create()
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_no_user(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.data),
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RewardListTestCase(BluebottleTestCase):
    def setUp(self):
        super(RewardListTestCase, self).setUp()
        self.client = JSONAPITestClient()
        self.user = BlueBottleUserFactory()
        self.initiative = InitiativeFactory.create()

        self.initiative.transitions.submit()
        self.initiative.transitions.approve()

        self.funding = FundingFactory.create(
            owner=self.user,
            initiative=self.initiative
        )

        self.create_url = reverse('funding-reward-list')
        self.funding_url = reverse('funding-detail', args=(self.funding.pk, ))

        self.data = {
            'data': {
                'type': 'activities/rewards',
                'attributes': {
                    'title': 'Test title',
                    'description': 'Test description',
                    'amount': {'amount': 100, 'currency': 'EUR'},
                    'limit': 10,
                },
                'relationships': {
                    'activity': {
                        'data': {
                            'type': 'activities/fundings',
                            'id': self.funding.pk,
                        }
                    }
                }
            }
        }

    def test_create(self):
        response = self.client.post(self.create_url, data=json.dumps(self.data), user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)

        self.assertEqual(
            data['data']['attributes']['description'],
            self.data['data']['attributes']['description']
        )
        self.assertEqual(
            data['data']['attributes']['title'],
            self.data['data']['attributes']['title']
        )

        response = self.client.get(self.funding_url)
        funding_data = json.loads(response.content)

        self.assertEqual(
            len(funding_data['data']['relationships']['rewards']['data']), 1
        )
        self.assertEqual(
            funding_data['data']['relationships']['rewards']['data'][0]['id'], unicode(data['data']['id'])
        )

    def test_create_wrong_currency(self):
        self.data['data']['attributes']['amount']['currency'] = 'USD'
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.data),
            user=BlueBottleUserFactory.create()
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_other_user(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.data),
            user=BlueBottleUserFactory.create()
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_no_user(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.data),
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FundingDetailTestCase(BluebottleTestCase):
    def setUp(self):
        super(FundingDetailTestCase, self).setUp()
        self.client = JSONAPITestClient()
        self.user = BlueBottleUserFactory()
        self.geolocation = GeolocationFactory.create(locality='Barranquilla')
        self.initiative = InitiativeFactory.create(
            owner=self.user,
            place=self.geolocation
        )

        self.initiative.transitions.submit()
        self.initiative.transitions.approve()
        self.initiative.save()

        self.funding = FundingFactory.create(
            initiative=self.initiative,
            owner=self.initiative.owner,
            target=Money(5000, 'EUR'),
            deadline=now() + timedelta(days=15)
        )

        self.funding_url = reverse('funding-detail', args=(self.funding.pk, ))

    def test_view_funding(self):
        DonationFactory.create_batch(5, amount=Money(200, 'EUR'), activity=self.funding, status='succeeded')
        DonationFactory.create_batch(2, amount=Money(100, 'EUR'), activity=self.funding, status='new')

        self.funding.amount_matching = Money(500, 'EUR')
        self.funding.save()

        response = self.client.get(self.funding_url, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)

        self.assertEqual(
            data['data']['attributes']['description'],
            self.funding.description
        )
        self.assertEqual(
            data['data']['attributes']['title'],
            self.funding.title
        )
        self.assertEqual(
            data['data']['attributes']['target'],
            {u'currency': u'EUR', u'amount': 5000.0}
        )
        self.assertEqual(
            data['data']['attributes']['amount-donated'],
            {u'currency': u'EUR', u'amount': 1000.0}
        )
        self.assertEqual(
            data['data']['attributes']['amount-matching'],
            {u'currency': u'EUR', u'amount': 500.0}
        )
        self.assertEqual(
            data['data']['attributes']['amount-raised'],
            {u'currency': u'EUR', u'amount': 1500.0}
        )

        # Should only see the three successful donations
        self.assertEqual(
            len(data['data']['relationships']['contributions']['data']),
            5
        )

        # Test that geolocation is included too
        geolocation = get_included(response, 'geolocations')
        self.assertEqual(geolocation['attributes']['locality'], 'Barranquilla')

    def test_get_bank_account(self):
        self.funding.bank_account = ExternalAccountFactory.create(
            account_id='some-external-account-id'
        )
        self.funding.save()

        connect_account = stripe.Account('some-connect-id')
        connect_account.update({
            'country': 'NL',
            'external_accounts': stripe.ListObject({
                'data': [connect_account]
            })
        })

        with mock.patch(
            'stripe.Account.retrieve', return_value=connect_account
        ):
            with mock.patch(
                'stripe.ListObject.retrieve', return_value=connect_account
            ):
                response = self.client.get(self.funding_url, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        bank_account = response.json()['data']['relationships']['bank-account']['data']
        self.assertEqual(
            bank_account['id'], unicode(self.funding.bank_account.pk)
        )

    def test_get_bank_account_other_user(self):
        self.funding.bank_account = ExternalAccountFactory.create(
            account_id='some-external-account-id'
        )
        self.funding.save()
        connect_account = stripe.Account('some-connect-id')
        connect_account.update({
            'country': 'NL',
            'external_accounts': stripe.ListObject({
                'data': [connect_account]
            })
        })

        with mock.patch(
            'stripe.Account.retrieve', return_value=connect_account
        ):
            with mock.patch(
                'stripe.ListObject.retrieve', return_value=connect_account
            ):
                response = self.client.get(self.funding_url, user=BlueBottleUserFactory.create())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('bank_account' not in response.json()['data']['relationships'])

    def test_update(self):
        new_title = 'New title'
        response = self.client.patch(
            self.funding_url,
            data=json.dumps({
                'data': {
                    'id': self.funding.pk,
                    'type': 'activities/fundings',
                    'attributes': {
                        'title': new_title,
                    }
                }
            }),
            user=self.user
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['data']['attributes']['title'],
            new_title
        )

    def test_update_bank_account(self):
        external_account = ExternalAccountFactory.create(
            account_id='some-external-account-id'
        )
        connect_account = stripe.Account('some-connect-id')
        connect_account.update({
            'country': 'NL',
            'external_accounts': stripe.ListObject({
                'data': [connect_account]
            })
        })

        with mock.patch(
            'stripe.Account.retrieve', return_value=connect_account
        ):
            with mock.patch(
                'stripe.ListObject.retrieve', return_value=connect_account
            ):
                response = self.client.patch(
                    self.funding_url,
                    data=json.dumps({
                        'data': {
                            'id': self.funding.pk,
                            'type': 'activities/fundings',
                            'relationships': {
                                'bank_account': {
                                    'data': {
                                        'id': external_account.pk,
                                        'type': 'payout-accounts/stripe-external-accounts'
                                    }
                                }
                            }
                        }
                    }),
                    user=self.user
                )
        self.assertEqual(response.status_code, 200)

        bank_account = response.json()['data']['relationships']['bank-account']['data']
        self.assertEqual(
            bank_account['id'], unicode(external_account.pk)
        )
        self.assertEqual(
            bank_account['type'], 'payout-accounts/stripe-external-accounts'
        )

    def test_update_other_user(self):
        response = self.client.patch(
            self.funding_url,
            data=json.dumps({
                'data': {
                    'id': self.funding.pk,
                    'type': 'activities/fundings',
                    'attributes': {
                        'title': 'new title',
                    }

                }
            }),
            user=BlueBottleUserFactory.create()
        )
        self.assertEqual(response.status_code, 403)


class FundraiserListTestCase(BluebottleTestCase):
    def setUp(self):
        super(FundraiserListTestCase, self).setUp()
        self.client = JSONAPITestClient()
        self.user = BlueBottleUserFactory()
        self.initiative = InitiativeFactory.create()

        self.initiative.transitions.submit()
        self.initiative.transitions.approve()
        self.initiative.save()

        self.funding = FundingFactory.create(
            initiative=self.initiative,
            deadline=now() + timedelta(days=15)
        )

        self.create_url = reverse('funding-fundraiser-list')
        self.funding_url = reverse('funding-detail', args=(self.funding.pk, ))

        self.data = {
            'data': {
                'type': 'activities/fundraisers',
                'attributes': {
                    'title': 'Test title',
                    'description': 'Test description',
                    'amount': {'amount': 100, 'currency': 'EUR'},
                    'deadline': str(now() + timedelta(days=10))
                },
                'relationships': {
                    'activity': {
                        'data': {
                            'type': 'activities/fundings',
                            'id': self.funding.pk,
                        }
                    }
                }
            }
        }

    def test_create(self):
        response = self.client.post(self.create_url, data=json.dumps(self.data), user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)

        self.assertEqual(
            data['data']['attributes']['description'],
            self.data['data']['attributes']['description']
        )
        self.assertEqual(
            data['data']['attributes']['title'],
            self.data['data']['attributes']['title']
        )
        self.assertEqual(
            data['data']['relationships']['owner']['data']['id'],
            unicode(self.user.pk)
        )

        response = self.client.get(self.funding_url)
        funding_data = json.loads(response.content)

        self.assertEqual(
            len(funding_data['data']['relationships']['fundraisers']['data']), 1
        )
        self.assertEqual(
            funding_data['data']['relationships']['fundraisers']['data'][0]['id'], data['data']['id']
        )

    def test_create_wrong_currency(self):
        self.data['data']['attributes']['amount']['currency'] = 'USD'
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.data),
            user=BlueBottleUserFactory.create()
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_deadline_to_long(self):
        self.data['data']['attributes']['deadline'] = unicode(self.funding.deadline + timedelta(days=1))
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.data),
            user=BlueBottleUserFactory.create()
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_other_user(self):
        # Should be allowed
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.data),
            user=BlueBottleUserFactory.create()
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_no_user(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.data),
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FundingTestCase(BluebottleTestCase):
    def setUp(self):
        super(FundingTestCase, self).setUp()
        self.client = JSONAPITestClient()
        self.user = BlueBottleUserFactory()
        self.initiative = InitiativeFactory.create(owner=self.user)

        self.create_url = reverse('funding-list')

        self.data = {
            'data': {
                'type': 'activities/fundings',
                'attributes': {
                    'title': 'test',
                },
                'relationships': {
                    'initiative': {
                        'data': {
                            'type': 'initiatives',
                            'id': self.initiative.pk,
                        }
                    }
                }
            }
        }

    def test_create(self):
        response = self.client.post(self.create_url, json.dumps(self.data), user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()
        self.assertTrue(
            data['data']['meta']['permissions']['PATCH']
        )
        self.assertTrue(
            get_included(response, 'geolocations')
        )

    def test_create_other_user(self):
        response = self.client.post(self.create_url, json.dumps(self.data), user=BlueBottleUserFactory.create())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DonationTestCase(BluebottleTestCase):
    def setUp(self):
        super(DonationTestCase, self).setUp()
        self.client = JSONAPITestClient()
        self.user = BlueBottleUserFactory()
        self.initiative = InitiativeFactory.create()

        self.initiative.transitions.submit()
        self.initiative.transitions.approve()

        self.funding = FundingFactory.create(initiative=self.initiative)

        self.create_url = reverse('funding-donation-list')
        self.funding_url = reverse('funding-detail', args=(self.funding.pk, ))

        self.data = {
            'data': {
                'type': 'contributions/donations',
                'attributes': {
                    'amount': {'amount': 100, 'currency': 'EUR'},
                },
                'relationships': {
                    'activity': {
                        'data': {
                            'type': 'activities/fundings',
                            'id': self.funding.pk,
                        }
                    }
                }
            }
        }

    def test_create(self):
        response = self.client.post(self.create_url, json.dumps(self.data), user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.loads(response.content)

        self.assertEqual(data['data']['attributes']['status'], DonationTransitions.values.new)
        self.assertEqual(data['data']['attributes']['amount'], {'amount': 100, 'currency': 'EUR'})
        self.assertEqual(data['data']['relationships']['activity']['data']['id'], unicode(self.funding.pk))
        self.assertEqual(data['data']['relationships']['user']['data']['id'], unicode(self.user.pk))
        self.assertIsNone(data['data']['attributes']['client-secret'])

    def test_donate(self):
        response = self.client.post(self.create_url, json.dumps(self.data), user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.loads(response.content)
        donation = Donation.objects.get(pk=data['data']['id'])
        donation.transitions.succeed()
        donation.save()

        response = self.client.get(self.funding_url, user=self.user)

        donation = get_included(response, 'contributions/donations')
        self.assertEqual(donation['relationships']['user']['data']['id'], unicode(self.user.pk))

    def test_donate_anonymous(self):
        self.data['data']['attributes']['anonymous'] = True
        response = self.client.post(self.create_url, json.dumps(self.data), user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.loads(response.content)

        self.assertEqual(data['data']['attributes']['status'], DonationTransitions.values.new)
        self.assertEqual(data['data']['attributes']['anonymous'], True)
        donation = Donation.objects.get(pk=data['data']['id'])
        self.assertTrue(donation.user, self.user)

        donation.transitions.succeed()
        donation.save()

        response = self.client.get(self.funding_url, user=self.user)

        donation = get_included(response, 'contributions/donations')
        self.assertFalse('user' in donation['relationships'])

    def test_update(self):
        response = self.client.post(self.create_url, json.dumps(self.data), user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.loads(response.content)

        update_url = reverse('funding-donation-detail', args=(data['data']['id'], ))

        patch_data = {
            'data': {
                'type': 'contributions/donations',
                'id': data['data']['id'],
                'attributes': {
                    'amount': {'amount': 200, 'currency': 'EUR'},
                },
            }
        }

        response = self.client.patch(update_url, json.dumps(patch_data), user=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)

        self.assertEqual(data['data']['attributes']['amount'], {'amount': 200, 'currency': 'EUR'})

    def test_update_change_user(self):
        response = self.client.post(self.create_url, json.dumps(self.data), user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.loads(response.content)

        update_url = reverse('funding-donation-detail', args=(data['data']['id'], ))

        patch_data = {
            'data': {
                'type': 'contributions/donations',
                'id': data['data']['id'],
                'relationships': {
                    'user': {
                        'data': {
                            'id': BlueBottleUserFactory.create().pk,
                            'type': 'members',
                        }
                    }
                },
            }
        }

        response = self.client.patch(update_url, json.dumps(patch_data), user=self.user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.content)

        self.assertEqual(
            data['errors'][0]['detail'],
            u'User can only be set, not changed.'
        )

    def test_update_wrong_user(self):
        response = self.client.post(self.create_url, json.dumps(self.data), user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.loads(response.content)

        update_url = reverse('funding-donation-detail', args=(data['data']['id'], ))

        patch_data = {
            'data': {
                'type': 'contributions/donations',
                'id': data['data']['id'],
                'attributes': {
                    'amount': {'amount': 200, 'currency': 'EUR'},
                },
            }
        }

        response = self.client.patch(update_url, json.dumps(patch_data), user=BlueBottleUserFactory.create())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_no_token(self):
        response = self.client.post(self.create_url, json.dumps(self.data), user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.loads(response.content)

        update_url = reverse('funding-donation-detail', args=(data['data']['id'], ))

        patch_data = {
            'data': {
                'type': 'contributions/donations',
                'id': data['data']['id'],
                'attributes': {
                    'amount': {'amount': 200, 'currency': 'EUR'},
                },
            }
        }

        response = self.client.patch(update_url, json.dumps(patch_data))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_no_user(self):
        response = self.client.post(self.create_url, json.dumps(self.data))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.loads(response.content)

        self.assertEqual(data['data']['attributes']['status'], DonationTransitions.values.new)
        self.assertEqual(data['data']['attributes']['amount'], {'amount': 100, 'currency': 'EUR'})
        self.assertEqual(len(data['data']['attributes']['client-secret']), 32)
        self.assertEqual(data['data']['relationships']['activity']['data']['id'], unicode(self.funding.pk))
        self.assertEqual(data['data']['relationships']['user']['data'], None)

    def test_claim(self):
        response = self.client.post(self.create_url, json.dumps(self.data))
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        update_url = reverse('funding-donation-detail', args=(data['data']['id'], ))
        patch_data = {
            'data': {
                'type': 'contributions/donations',
                'id': data['data']['id'],
                'relationships': {
                    'user': {
                        'data': {
                            'id': self.user.pk,
                            'type': 'members',
                        }
                    }
                },
            }
        }

        response = self.client.patch(
            update_url,
            json.dumps(patch_data),
            HTTP_AUTHORIZATION='Donation {}'.format(data['data']['attributes']['client-secret'])
        )
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data['data']['attributes']['status'], DonationTransitions.values.new)
        self.assertEqual(data['data']['attributes']['amount'], {'amount': 100, 'currency': 'EUR'})
        self.assertEqual(data['data']['relationships']['user']['data']['id'], unicode(self.user.pk))
        self.assertTrue('client-secret' not in data['data']['attributes'])

        patch_data = {
            'data': {
                'type': 'contributions/donations',
                'id': data['data']['id'],
                'attributes': {
                    'amount': {'amount': 200, 'currency': 'EUR'},
                },
            }
        }

        response = self.client.patch(
            update_url,
            json.dumps(patch_data),
            user=self.user
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_claim_authorized(self):
        response = self.client.post(self.create_url, json.dumps(self.data))
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        update_url = reverse('funding-donation-detail', args=(data['data']['id'], ))
        patch_data = {
            'data': {
                'type': 'contributions/donations',
                'id': data['data']['id'],
                'relationships': {
                    'user': {
                        'data': {
                            'id': self.user.pk,
                            'type': 'members',
                        }
                    }
                },
            }
        }

        response = self.client.patch(
            update_url,
            json.dumps(patch_data),
            user=self.user
        )
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_no_user(self):
        response = self.client.post(self.create_url, json.dumps(self.data))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.loads(response.content)
        update_url = reverse('funding-donation-detail', args=(data['data']['id'], ))

        patch_data = {
            'data': {
                'type': 'contributions/donations',
                'id': data['data']['id'],
                'attributes': {
                    'amount': {'amount': 200, 'currency': 'EUR'},
                },
            }
        }

        response = self.client.patch(
            update_url,
            json.dumps(patch_data),
            HTTP_AUTHORIZATION='Donation {}'.format(data['data']['attributes']['client-secret'])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data['data']['attributes']['amount'], {'amount': 200, 'currency': 'EUR'})

    def test_update_no_user_set_user(self):
        response = self.client.post(self.create_url, json.dumps(self.data))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.loads(response.content)
        update_url = reverse('funding-donation-detail', args=(data['data']['id'], ))

        patch_data = {
            'data': {
                'type': 'contributions/donations',
                'id': data['data']['id'],
                'attributes': {
                    'amount': {'amount': 200, 'currency': 'EUR'},
                },
                'relationships': {
                    'user': {
                        'data': {
                            'id': self.user.pk,
                            'type': 'members',
                        }
                    }
                }
            }
        }

        response = self.client.patch(
            update_url,
            json.dumps(patch_data),
            HTTP_AUTHORIZATION='Donation {}'.format(data['data']['attributes']['client-secret'])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data['data']['attributes']['amount'], {'amount': 200, 'currency': 'EUR'})
        self.assertEqual(data['data']['relationships']['user']['data']['id'], unicode(self.user.pk))

    def test_update_no_user_wrong_token(self):
        response = self.client.post(self.create_url, json.dumps(self.data))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.loads(response.content)
        update_url = reverse('funding-donation-detail', args=(data['data']['id'], ))

        patch_data = {
            'data': {
                'type': 'contributions/donations',
                'id': data['data']['id'],
                'attributes': {
                    'amount': {'amount': 200, 'currency': 'EUR'},
                },
            }
        }

        response = self.client.patch(
            update_url,
            json.dumps(patch_data),
            HTTP_AUTHORIZATION='Donation wrong-token'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_fundraiser(self):
        fundraiser = FundraiserFactory.create(activity=self.funding)
        self.data['data']['relationships']['fundraiser'] = {
            'data': {'id': fundraiser.pk, 'type': 'activities/fundraisers'}
        }

        response = self.client.post(self.create_url, json.dumps(self.data), user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.loads(response.content)

        self.assertEqual(data['data']['relationships']['fundraiser']['data']['id'], unicode(fundraiser.pk))

    def test_create_fundraiser_unrelated(self):
        fundraiser = FundraiserFactory.create()
        self.data['data']['relationships']['fundraiser'] = {
            'data': {'id': fundraiser.pk, 'type': 'activities/fundraisers'}
        }

        response = self.client.post(self.create_url, json.dumps(self.data), user=self.user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reward(self):
        reward = RewardFactory.create(amount=Money(100, 'EUR'), activity=self.funding)
        self.data['data']['relationships']['reward'] = {
            'data': {'id': reward.pk, 'type': 'activities/rewards'}
        }
        response = self.client.post(self.create_url, json.dumps(self.data), user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.loads(response.content)

        self.assertEqual(data['data']['relationships']['reward']['data']['id'], unicode(reward.pk))

    def test_create_reward_higher_amount(self):
        reward = RewardFactory.create(amount=Money(50, 'EUR'), activity=self.funding)
        self.data['data']['relationships']['reward'] = {
            'data': {'id': reward.pk, 'type': 'activities/rewards'}
        }
        response = self.client.post(self.create_url, json.dumps(self.data), user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.loads(response.content)

        self.assertEqual(data['data']['relationships']['reward']['data']['id'], unicode(reward.pk))

    def test_create_reward_lower_amount(self):
        reward = RewardFactory.create(amount=Money(150, 'EUR'), activity=self.funding)
        self.data['data']['relationships']['reward'] = {
            'data': {'id': reward.pk, 'type': 'activities/rewards'}
        }
        response = self.client.post(self.create_url, json.dumps(self.data), user=self.user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reward_wrong_activity(self):
        reward = RewardFactory.create(amount=Money(100, 'EUR'))
        self.data['data']['relationships']['reward'] = {
            'data': {'id': reward.pk, 'type': 'activities/rewards'}
        }
        response = self.client.post(self.create_url, json.dumps(self.data), user=self.user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CurrencySettingsTestCase(BluebottleTestCase):
    def setUp(self):
        super(CurrencySettingsTestCase, self).setUp()
        self.settings_url = reverse('settings')
        StripePaymentProviderFactory.create()
        flutterwave_provider = FlutterwavePaymentProviderFactory.create()
        cur = flutterwave_provider.paymentcurrency_set.first()
        cur.min_amount = 1000
        cur.default1 = 1000
        cur.default2 = 2000
        cur.default3 = 5000
        cur.default4 = 10000
        cur.save()

    def test_create(self):
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['platform']['currencies'],
            [
                {
                    'code': 'EUR',
                    'name': 'Euro',
                    'max_amount': None,
                    'symbol': u'\u20ac',
                    'min_amount': 5.00,
                    'default_amounts': [10.00, 20.00, 50.00, 100.00],
                    'provider': 'stripe'
                },
                {
                    'code': 'USD',
                    'name': 'US Dollar',
                    'max_amount': None,
                    'symbol': '$',
                    'min_amount': 5.00,
                    'default_amounts': [10.00, 20.00, 50.00, 100.00],
                    'provider': 'stripe'
                },
                {
                    'code': 'NGN',
                    'name': 'Nigerian Naira',
                    'max_amount': None,
                    'symbol': u'\u20a6',
                    'min_amount': 1000.00,
                    'default_amounts': [1000.00, 2000.00, 5000.00, 10000.00],
                    'provider': 'flutterwave'
                }
            ]
        )
