# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-09-04 06:38
from __future__ import unicode_literals

from django.db import migrations


def map_donation_status(status):
    mapping = {
        'failed': 'failed',
        'cancelled': 'failed',
        'success': 'succeeded',
        'created': 'new',
        'locked': 'new',
        'in_progress': 'new',
        'refunded': 'refunded',
        'pending': 'succeeded',
        'pledged': 'succeeded',
        'refund_requested': 'refunded'
    }
    return mapping[status]


def map_payment_status(status):
    mapping = {
        'created': 'new',
        'started': 'new',
        'cancelled': 'failed',
        'pledged': 'succeeded',
        'settled': 'succeeded',
        'charged_back': 'refunded',
        'refund_requested': 'refund_requested',
        'refunded': 'refunded',
        'failed': 'failed',
        'in_progress': 'new',
        'authorized': 'pending',
        'unknown': 'failed'
    }
    return mapping[status]


def get_latest_order_payment(order):
    if order.order_payments.filter(status__in=['settled', 'authorized']).count():
        return order.order_payments.filter(status__in=['settled', 'authorized']).order_by('-created').first()
    return order.order_payments.first()


def migrate_orders(apps, schema_editor):

    ContentType = apps.get_model('contenttypes', 'ContentType')
    Order = apps.get_model('orders', 'Order')
    Funding = apps.get_model('funding', 'Funding')
    Payment = apps.get_model('payments', 'Payment')
    NewDonation = apps.get_model('funding', 'Donation')
    LegacyPayment = apps.get_model('funding', 'LegacyPayment')
    StripeSourcePayment = apps.get_model('funding_stripe', 'StripeSourcePayment')
    PledgePayment = apps.get_model('funding_pledge', 'PledgePayment')
    FlutterwavePayment = apps.get_model('funding_flutterwave', 'FlutterwavePayment')
    LipishaPayment = apps.get_model('funding_lipisha', 'LipishaPayment')
    VitepayPayment = apps.get_model('funding_vitepay', 'VitepayPayment')
    Wallpost = apps.get_model('wallposts', 'Wallpost')

    stripe_content_type = ContentType.objects.get_for_model(StripeSourcePayment)
    pledge_content_type = ContentType.objects.get_for_model(PledgePayment)
    flutterwave_content_type = ContentType.objects.get_for_model(FlutterwavePayment)
    vitepay_content_type = ContentType.objects.get_for_model(VitepayPayment)
    lipisha_content_type = ContentType.objects.get_for_model(LipishaPayment)
    legacy_content_type = ContentType.objects.get_for_model(LegacyPayment)
    donation_content_type = ContentType.objects.get_for_model(NewDonation)

    for order in Order.objects.iterator():
        order_payment = get_latest_order_payment(order)
        for donation in order.donations.prefetch_related('project').all():
            try:
                funding = Funding.objects.prefetch_related('rewards').get(slug=donation.project.slug)
            except Funding.DoesNotExist:
                print donation.project.title
                print donation.id
                continue
            reward_id = None
            if donation.reward:
                reward_id = donation.reward.new_reward_id
            new_donation = NewDonation.objects.create(
                user_id=order.user_id,
                polymorphic_ctype=donation_content_type,
                activity=funding,
                created=donation.created,
                amount=donation.amount,
                name=donation.name,
                status=map_donation_status(order.status),
                reward_id=reward_id,
                # fundraiser=fundraiser,
                anonymous=donation.anonymous
            )

            # Store reference to new donation on old one
            donation.new_donation_id = new_donation.id
            donation.save()

            payment= None
            if order_payment:
                try:
                    payment = order_payment.payment
                except Payment.DoesNotExist:
                    pass

            if order_payment and payment:
                unique_id = "order-payment-".format(order_payment.id)
                if 'stripe' in payment.polymorphic_ctype.model:
                    new_payment = StripeSourcePayment.objects.create(
                        created=payment.created,
                        polymorphic_ctype=stripe_content_type,
                        donation=new_donation,
                        source_token=order_payment.payment.stripepayment.source_token,
                        charge_token=order_payment.payment.stripepayment.charge_token,
                        status=map_payment_status(order_payment.payment.status)
                    )
                elif 'pledge' in order_payment.payment_method:
                    new_payment = PledgePayment.objects.create(
                        polymorphic_ctype=pledge_content_type,
                        created=payment.created,
                        donation=new_donation,
                        status=map_payment_status(order_payment.payment.status)
                    )
                elif 'flutterwave' in payment.polymorphic_ctype.model:
                    new_payment = FlutterwavePayment.objects.create(
                        polymorphic_ctype=flutterwave_content_type,
                        created=payment.created,
                        donation=new_donation,
                        tx_ref=order_payment.payment.flutterwavepayment.transaction_reference or unique_id,
                        status=map_payment_status(order_payment.payment.status)
                    )
                elif 'vitepay' in payment.polymorphic_ctype.model:
                    new_payment = VitepayPayment.objects.create(
                        polymorphic_ctype=vitepay_content_type,
                        created=payment.created,
                        donation=new_donation,
                        status=map_payment_status(order_payment.payment.status),
                        unique_id=unique_id,
                        payment_url = order_payment.payment.vitepaypayment.payment_url
                    )
                elif 'lipisha' in payment.polymorphic_ctype.model:
                    new_payment = LipishaPayment.objects.create(
                        polymorphic_ctype=lipisha_content_type,
                        created=payment.created,
                        donation=new_donation,
                        mobile_number=order_payment.payment.lipishapayment.transaction_mobile_number,
                        transaction=order_payment.payment.lipishapayment.transaction_reference,
                        unique_id=order_payment.payment.lipishapayment.reference or unique_id,
                        status=map_payment_status(order_payment.payment.status)
                    )
                else:
                    new_payment = LegacyPayment.objects.create(
                        polymorphic_ctype=legacy_content_type,
                        created=payment.created,
                        donation=new_donation,
                        method=order_payment.payment_method,
                        status=map_payment_status(order_payment.payment.status),
                        data=order_payment.payment.__dict__
                    )

    for wp in Wallpost.objects.select_related('donation').filter(donation__isnull=False).all():
        wp.funding_donation_id = wp.donation.new_donation_id
        wp.save()


def wipe_donations(apps, schema_editor):

    Donation = apps.get_model('funding', 'Donation')
    Payment = apps.get_model('funding', 'Payment')

    Donation.objects.all().delete()
    Payment.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20180509_1437'),
        ('donations', '0011_auto_20191101_1046'),
        ('projects', '0091_project_to_initiatives'),
        ('funding_flutterwave', '0003_flutterwavepayoutaccount'),
        ('funding_stripe', '0001_initial'),
        ('wallposts', '0019_auto_20191017_2204'),
        ('rewards', '0009_auto_20191104_1230')
    ]

    operations = [
        migrations.RunPython(migrate_orders, wipe_donations)
    ]
