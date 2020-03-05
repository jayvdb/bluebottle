from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


from bluebottle.auth.views import GetAuthToken
from bluebottle.utils.views import LoginWithView

urlpatterns = [
    url(r'^api/config',
        include('bluebottle.clients.urls.api')),
    url(r'^api/redirects/?',
        include('bluebottle.redirects.urls.api')),
    url(r'^api/users/',
        include('bluebottle.bb_accounts.urls.api')),
    url(r'^api/bb_projects/',
        include('bluebottle.bb_projects.urls.api')),
    url(r'^api/fundraisers/',
        include('bluebottle.bb_fundraisers.urls.api')),
    url(r'^api/categories/',
        include('bluebottle.categories.urls.api')),
    url(r'^api/bb_tasks/',
        include('bluebottle.bb_tasks.urls.api')),
    url(r'^downloads/',
        include('bluebottle.bb_tasks.urls.media')),
    url(r'^api/geo/',
        include('bluebottle.geo.urls.api')),
    url(r'^api/news/',
        include('bluebottle.news.urls.api')),
    url(r'^api/pages/',
        include('bluebottle.pages.urls.api')),
    url(r'^api/quotes/',
        include('bluebottle.quotes.urls.api')),
    url(r'^api/slides/',
        include('bluebottle.slides.urls.api')),
    url(r'^api/utils/',
        include('bluebottle.utils.urls.api')),
    url(r'^api/wallposts/',
        include('bluebottle.wallposts.urls.api')),
    url(r'^api/terms/',
        include('bluebottle.terms.urls.api')),
    url(r'^api/metadata/',
        include('bluebottle.utils.urls.api')),
    url(r'^api/orders/',
        include('bluebottle.bb_orders.urls.api')),
    url(r'^api/donations/',
        include('bluebottle.donations.urls.api')),
    url(r'^api/order_payments/',
        include('bluebottle.payments.urls.order_payments_api')),
    url(r'^api/payments/',
        include('bluebottle.payments.urls.api')),
    url(r'^api/rewards/',
        include('bluebottle.rewards.urls.api')),

    # Homepage API urls
    url(r'^api/homepage/',
        include('bluebottle.homepage.urls.api')),
    url(r'^api/stats',
        include('bluebottle.statistics.urls.api')),
    url(r'^api/bb_projects/',
        include('bluebottle.projects.urls.api')),
    url(r'^api/cms/',
        include('bluebottle.cms.urls.api')),
    url(r'^api/initiatives',
        include('bluebottle.initiatives.urls.api')),

    url(r'^api/activities',
        include('bluebottle.activities.urls.api')),

    url(r'^api/events',
        include('bluebottle.events.urls.api')),

    url(r'^api/assignments',
        include('bluebottle.assignments.urls.api')),

    url(r'^api/funding',
        include('bluebottle.funding.urls.api')),
    url(r'^api/funding',
        include('bluebottle.funding.urls.api')),
    url(r'^api/funding/pledge',
        include('bluebottle.funding_pledge.urls.api')),
    url(r'^api/funding/stripe',
        include('bluebottle.funding_stripe.urls.api')),
    url(r'^api/funding/vitepay',
        include('bluebottle.funding_vitepay.urls.api')),
    url(r'^api/funding/flutterwave',
        include('bluebottle.funding_flutterwave.urls.api')),
    url(r'^api/funding/lipisha',
        include('bluebottle.funding_lipisha.urls.api')),

    url(r'^api/files/',
        include('bluebottle.files.urls.api')),

    url(r'^payments_mock/',
        include('bluebottle.payments_mock.urls.core')),
    url(r'^payments_docdata/',
        include('bluebottle.payments_docdata.urls.core')),
    url(r'^payments_interswitch/',
        include('bluebottle.payments_interswitch.urls.core')),
    url(r'^payments_vitepay/',
        include('bluebottle.payments_vitepay.urls.core')),
    url(r'^payments_flutterwave/',
        include('bluebottle.payments_flutterwave.urls.core')),
    url(r'^payments_lipisha/',
        include('bluebottle.payments_lipisha.urls.core')),
    url(r'^payments_beyonic/',
        include('bluebottle.payments_beyonic.urls.core')),
    url(r'^payments_stripe/',
        include('bluebottle.payments_stripe.urls.core')),
    url(r'^payouts_stripe/',
        include('bluebottle.payouts.urls.stripe')),

    url(r'^surveys/',
        include('bluebottle.surveys.urls.core')),

    url(r'^api/suggestions/',
        include('bluebottle.suggestions.urls.api')),

    url(r'^api/votes/',
        include('bluebottle.votes.urls.api')),
    url(r'^api/surveys/',
        include('bluebottle.surveys.urls.api')),

    url(r'^api/organizations',
        include('bluebottle.organizations.urls.api')),

    # JSON Web Token based authentication for Django REST framework
    url(r'^api/token-auth/', obtain_jwt_token, name='token-auth'),

    url(r'^api/token-auth-refresh/$', refresh_jwt_token),

    # Social token authorization
    url(r'^api/social/',
        include('bluebottle.social.urls.api')),

    url(r'token/', include('bluebottle.token_auth.urls')),

    # urls for payout service
    url(r'^api/projects/',
        include('bluebottle.projects.urls.api')),
    url(r'^api/payouts/',
        include('bluebottle.payouts_dorado.urls')),
    url(r'^api/payouts/',
        include('bluebottle.payouts.urls.api')),

    url(r'^api/scim/v2/', include('bluebottle.scim.urls.api')),

    url(r'^downloads/', include('bluebottle.payouts.urls.media')),
    url(r'^login-with/(?P<user_id>[0-9]+)/(?P<token>[0-9A-Za-z:\-_]{1,200})',
        LoginWithView.as_view(), name='login-with'),

    url(r'^downloads/', include('bluebottle.projects.urls.media')),

]


# Nicely parse 500 errors so we get semantic messages in tests.
def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


# Serve django-staticfiles (only works in DEBUG)
# https://docs.djangoproject.com/en/dev/howto/static-files/#serving-static-files-in-development
urlpatterns += staticfiles_urlpatterns()

# Serve media files (only works in DEBUG)
# https://docs.djangoproject.com/en/dev/howto/static-files/#django.conf.urls.static.static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [

    url('', include('social_django.urls',
                    namespace='social')),
    url(r'^api/social-login/(?P<backend>[^/]+)/$',
        GetAuthToken.as_view()),

    # Needed for the self-documenting API in Django Rest Framework.
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),

    url(r'^', include('django.conf.urls.i18n')),
]
