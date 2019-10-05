# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-07-18 07:04
from __future__ import unicode_literals

from django.db import migrations, connection
from django.contrib.gis.geos import Point

from bluebottle.clients import properties


def map_status(status):
    mapping = {
        'plan-new': 'draft',
        'plan-submitted': 'submitted',
        'plan-needs-work': 'needs_work',
        'voting': 'approved',
        'voting-done': 'approved',
        'campaign': 'approved',
        'to-be-continued': 'approved',
        'done-complete': 'approved',
        'done-incomplete': 'approved',
        'closed': 'closed',
        'refunded': 'approved',
    }
    return mapping[status.slug]


def map_funding_status(status):
    mapping = {
        'plan-new': 'in_review',
        'plan-submitted': 'in_review',
        'plan-needs-work': 'in_review',
        'voting': 'open',
        'voting-done': 'open',
        'campaign': 'open',
        'to-be-continued': 'open',
        'done-complete': 'succeeded',
        'done-incomplete': 'succeeded',
        'closed': 'closed',
        'refunded': 'refunded',
    }
    return mapping[status.slug]


def map_funding_review_status(status):
    mapping = {
        'plan-new': 'draft',
        'plan-submitted': 'submitted',
        'plan-needs-work': 'needs_work',
        'voting': 'approved',
        'voting-done': 'approved',
        'campaign': 'approved',
        'to-be-continued': 'approved',
        'done-complete': 'approved',
        'done-incomplete': 'approved',
        'closed': 'approved',
        'refunded': 'approved',
    }
    return mapping[status.slug]


def truncate(number, limit):
    return int(number * pow(10, limit)) / 10 ^ pow(10, limit)


def set_currencies(apps, provider, name):
    PaymentCurrency = apps.get_model('funding', 'PaymentCurrency')
    defaults = properties.DONATION_AMOUNTS
    for method in properties.PAYMENT_METHODS:
        if method['provider'] == name:
            for cur in method['currencies']:
                val = method['currencies'][cur]
                PaymentCurrency.objects.get_or_create(
                    provider=provider,
                    code=cur,
                    defaults={
                        'min_amount': getattr(val, 'min_amount', 5.0),
                        'default1': defaults[cur][0],
                        'default2': defaults[cur][1],
                        'default3': defaults[cur][2],
                        'default4': defaults[cur][3],
                    }
                )


def migrate_payment_providers(apps):

    PledgePaymentProvider = apps.get_model('funding_pledge', 'PledgePaymentProvider')
    StripePaymentProvider = apps.get_model('funding_stripe', 'StripePaymentProvider')
    FlutterwavePaymentProvider = apps.get_model('funding_flutterwave', 'FlutterwavePaymentProvider')
    VitepayPaymentProvider = apps.get_model('funding_vitepay', 'VitepayPaymentProvider')
    LipishaPaymentProvider = apps.get_model('funding_lipisha', 'LipishaPaymentProvider')

    Client = apps.get_model('clients', 'Client')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    tenant = Client.objects.get(schema_name=connection.tenant.schema_name)
    properties.set_tenant(tenant)

    for provider in properties.MERCHANT_ACCOUNTS:
        pp = None
        if provider['merchant'] == 'stripe':
            content_type = ContentType.objects.get_for_model(StripePaymentProvider)
            pp = StripePaymentProvider.objects.create(
                polymorphic_ctype=content_type,
            )
            for payment_methods in properties.PAYMENT_METHODS:
                if payment_methods['id'] == 'stripe-creditcard':
                    pp.credit_card = True
                elif payment_methods['id'] == 'stripe-ideal':
                    pp.ideal = True
                elif payment_methods['id'] == 'stripe-directdebit':
                    pp.direct_debit = True
                elif payment_methods['id'] == 'stripe-bancontact':
                    pp.bancontact = True
            pp.save()
            set_currencies(apps, pp, 'stripe')

        elif provider['merchant'] == 'vitepay':
            content_type = ContentType.objects.get_for_model(VitepayPaymentProvider)
            pp = VitepayPaymentProvider.objects.create(
                polymorphic_ctype=content_type,
                api_secret=provider['api_secret'],
                api_key=provider['api_key'],
                api_url=provider['api_url'],
                prefix='new'
            )
            set_currencies(apps, pp, 'vitepay')
        elif provider['merchant'] == 'lipisha':
            content_type = ContentType.objects.get_for_model(LipishaPaymentProvider)
            pp = LipishaPaymentProvider.objects.create(
                polymorphic_ctype=content_type,
                api_key=provider['api_key'],
                api_signature=provider['api_signature'],
                paybill=provider['business_number'],
                prefix='new'
            )
            set_currencies(apps, pp, 'lipisha')
        elif provider['merchant'] == 'flutterwave':
            content_type = ContentType.objects.get_for_model(FlutterwavePaymentProvider)
            pp = FlutterwavePaymentProvider.objects.create(
                polymorphic_ctype=content_type,
                pub_key=provider['pub_key'],
                sec_key=provider['sec_key'],
                prefix='new'
            )
            set_currencies(apps, pp, 'flutterwave')
        elif provider['merchant'] == 'pledge':
            content_type = ContentType.objects.get_for_model(PledgePaymentProvider)
            pp = PledgePaymentProvider.objects.create(
                polymorphic_ctype=content_type,
            )
            set_currencies(apps, pp, 'pledge')


def migrate_projects(apps, schema_editor):
    migrate_payment_providers(apps)

    Project = apps.get_model('projects', 'Project')
    Initiative = apps.get_model('initiatives', 'Initiative')
    Funding = apps.get_model('funding', 'Funding')
    Geolocation = apps.get_model('geo', 'Geolocation')
    Country = apps.get_model('geo', 'Country')
    Image = apps.get_model('files', 'Image')
    Client = apps.get_model('clients', 'Client')
    OrganizationContact = apps.get_model('organizations', 'OrganizationContact')
    StripePayoutAccount = apps.get_model('funding_stripe', 'StripePayoutAccount')
    ExternalAccount = apps.get_model('funding_stripe', 'ExternalAccount')
    PlainPayoutAccount = apps.get_model('funding', 'PlainPayoutAccount')
    PayoutAccount = apps.get_model('funding', 'PayoutAccount')
    OldPayoutAccount = apps.get_model('payouts', 'PayoutAccount')
    FlutterwaveBankAccount = apps.get_model('funding_flutterwave', 'FlutterwaveBankAccount')
    VitepayBankAccount = apps.get_model('funding_vitepay', 'VitepayBankAccount')
    LipishaBankAccount = apps.get_model('funding_lipisha', 'LipishaBankAccount')

    ContentType = apps.get_model('contenttypes', 'ContentType')

    # Clean-up previous migrations of projects to initiatives
    Initiative.objects.all().delete()

    tenant = Client.objects.get(schema_name=connection.tenant.schema_name)
    properties.set_tenant(tenant)

    for project in Project.objects.all():

        if hasattr(project, 'projectlocation') and project.projectlocation.country:
            if project.projectlocation.latitude and project.projectlocation.longitude:
                point = Point(
                    truncate(project.projectlocation.longitude, 12),
                    truncate(project.projectlocation.latitude, 12)
                )
            else:
                point = Point(0, 0)

            country = project.country

            if not country and project.projectlocation.country and Country.objects.filter(
                    translations__name=project.projectlocation.country
                ).count():
                country = Country.objects.filter(
                    translations__name__contains=project.projectlocation.country
                ).first()

            if not country:
                country = Country.objects.filter(alpha2_code=properties.DEFAULT_COUNTRY_CODE).first()

            if country:
                place = Geolocation.objects.create(
                    street=project.projectlocation.street,
                    postal_code=project.projectlocation.postal_code,
                    country=country,
                    locality=project.projectlocation.city,
                    position=point
                )
            else:
                place = None
        else:
            if project.country:
                place = Geolocation.objects.create(
                    country=project.country,
                    position=Point(0, 0)
                )
            else:
                place = None

        initiative = Initiative.objects.create(
            title=project.title,
            slug=project.slug,
            pitch=project.pitch or '',
            story=project.story or '',
            theme=project.theme,
            video_url=project.video_url,
            place=place,
            location=project.location,
            owner=project.owner,
            reviewer=project.reviewer,
            activity_manager=project.task_manager,
            promoter=project.promoter,
            status=map_status(project.status)

        )
        if project.image:
            try:
                image = Image.objects.create(owner=project.owner)
                image.file.save(project.image.name, project.image.file, save=True)
                initiative.image = image
            except IOError:
                pass

        if project.organization:
            initiative.organization = project.organization

        contact = OrganizationContact.objects.filter(organization=project.organization).first()
        if contact:
            initiative.organization_contact = contact

        initiative.created = project.created
        initiative.categories = project.categories.all()
        initiative.save()

        # Create Funding event if there are donations
        if project.project_type in ['both', 'funding'] \
                or project.donation_set.count() \
                or project.amount_asked.amount:
            account = None
            if project.payout_account:
                try:
                    stripe_account = project.payout_account.stripepayoutaccount
                    content_type = ContentType.objects.get_for_model(StripePayoutAccount)
                    payout_account = StripePayoutAccount.objects.create(
                        polymorphic_ctype=content_type,
                        account_id=stripe_account.account_id or 'unknown',
                        owner=stripe_account.user,
                        # country=stripe_account.country.alpha2_code
                    )
                    content_type = ContentType.objects.get_for_model(ExternalAccount)
                    account = ExternalAccount.objects.create(
                        polymorphic_ctype=content_type,
                        connect_account=payout_account,
                        # account_id=stripe_account.bank_details.account
                    )
                except OldPayoutAccount.DoesNotExist:
                    content_type = ContentType.objects.get_for_model(PlainPayoutAccount)
                    plain_account = project.payout_account.plainpayoutaccount
                    payout_account = PlainPayoutAccount.objects.create(
                        polymorphic_ctype=content_type,
                        owner=plain_account.user,
                        reviewed=plain_account.reviewed
                    )

                    if str(project.amount_asked.currency) == 'NGN':
                        content_type = ContentType.objects.get_for_model(FlutterwaveBankAccount)
                        country = None
                        if plain_account.account_bank_country:
                            country = plain_account.account_bank_country.alpha2_code
                        account = FlutterwaveBankAccount.objects.create(
                            polymorphic_ctype=content_type,
                            connect_account=payout_account,
                            account_holder_name=plain_account.account_holder_name,
                            bank_country_code=country,
                            account_number=plain_account.account_number
                        )

                    if str(project.amount_asked.currency) == 'KES':
                        content_type = ContentType.objects.get_for_model(LipishaBankAccount)
                        account = LipishaBankAccount.objects.create(
                            polymorphic_ctype=content_type,
                            connect_account=payout_account,
                            account_number=plain_account.account_number,
                            account_name=plain_account.account_holder_name,
                            address=plain_account.account_holder_address
                        )

                    if str(project.amount_asked.currency) == 'CFA':
                        content_type = ContentType.objects.get_for_model(VitepayBankAccount)
                        account = VitepayBankAccount.objects.create(
                            polymorphic_ctype=content_type,
                            connect_account=payout_account,
                            account_name=plain_account.account_holder_name,
                        )

            content_type = ContentType.objects.get_for_model(Funding)
            funding = Funding.objects.create(
                # Common activity fields
                polymorphic_ctype=content_type,  # This does not get set automatically in migrations
                initiative=initiative,
                owner=project.owner,
                highlight=project.is_campaign,
                created=project.created,
                updated=project.updated,
                status=map_funding_status(project.status),
                review_status=map_funding_review_status(project.status),
                title=project.title,
                slug=project.slug,
                description=project.pitch or '',

                # Funding specific fields
                deadline=project.deadline,
                # ??? duration
                target=project.amount_asked,
                amount_matching=project.amount_extra,
                country=project.country,
                bank_account=account
            )

            # TODO: Add budget lines
            # TODO: Add fundraisers
            # TODO: Add rewards


def wipe_initiatives(apps, schema_editor):

    Initiative = apps.get_model('initiatives', 'Initiative')
    Funding = apps.get_model('funding', 'Funding')
    PaymentProvider = apps.get_model('funding', 'PaymentProvider')

    PaymentProvider.objects.all().delete()
    Initiative.objects.all().delete()
    Funding.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0090_merge_20190222_1101'),
        ('funding', '0035_auto_20191002_1415'),
        ('funding_lipisha', '0006_auto_20191001_2251'),
        ('funding_vitepay', '0007_auto_20191002_0903'),
        ('funding_flutterwave', '0005_auto_20191002_0903'),
        ('funding_stripe', '0001_initial'),
        ('funding_pledge', '0002_pledgepaymentprovider'),
    ]

    operations = [
        migrations.RunPython(migrate_projects, wipe_initiatives)
    ]
