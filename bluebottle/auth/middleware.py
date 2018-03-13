from calendar import timegm
from datetime import datetime, timedelta
import json
import logging

from bluebottle.common.models import CommonPlatformSettings
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http.response import HttpResponse
from django.utils import timezone
from django.http.request import RawPostDataException

from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from lockdown.middleware import LockdownMiddleware as BaseLockdownMiddleware, compile_url_exceptions

from bluebottle.utils.utils import get_client_ip


LAST_SEEN_DELTA = 10  # in minutes


def isAdminRequest(request):
    parts = request.path.split('/')
    base_path = None
    if len(parts) > 2:
        base_path = parts[2]
    return request.path.startswith('/downloads') or base_path in ['jet', 'admin']


class UserJwtTokenMiddleware:
    """
    Custom middleware to set the User on the request when using
    Jwt Token authentication.
    """

    def process_request(self, request):
        """ Override only the request to add the user """
        try:
            return request.user
        except AttributeError:
            pass

        obj = JSONWebTokenAuthentication()

        try:
            user_auth_tuple = obj.authenticate(request)
        except exceptions.APIException:
            user_auth_tuple = None

        if user_auth_tuple is not None:
            request.user, _ = user_auth_tuple

            # Set last_seen on the user record if it has been > 10 mins
            # since the record was set.
            if not request.user.last_seen or (request.user.last_seen <
               timezone.now() - timedelta(minutes=LAST_SEEN_DELTA)):
                request.user.last_seen = timezone.now()
                request.user.save()
            return


class SlidingJwtTokenMiddleware:
    """
    Custom middleware to set a sliding window for the jwt auth token expiration.
    """

    def process_response(self, request, response):
        """ Override only the request to add the new token """
        obj = JSONWebTokenAuthentication()

        try:
            user_auth_tuple = obj.authenticate(request)
        except exceptions.APIException:
            user_auth_tuple = None

        # Check if request includes valid token
        if user_auth_tuple is not None:
            user, _auth = user_auth_tuple

            # Get the payload details
            jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
            payload = jwt_decode_handler(_auth)
            logging.debug('JWT payload found: {0}'.format(payload))

            # Check whether we need to renew the token. This will happen if the token
            # hasn't been renewed in JWT_TOKEN_RENEWAL_DELTA
            exp = payload.get('exp')
            created_timestamp = exp - int(
                api_settings.JWT_EXPIRATION_DELTA.total_seconds())
            renewal_timestamp = created_timestamp + int(
                settings.JWT_TOKEN_RENEWAL_DELTA.total_seconds())
            now_timestamp = timegm(datetime.utcnow().utctimetuple())

            # If it has been less than JWT_TOKEN_RENEWAL_DELTA time since the
            # token was created then we will pass on created a renewed token
            # and just return the response unchanged.
            if now_timestamp < renewal_timestamp:
                logging.debug(
                    'JWT_TOKEN_RENEWAL_DELTA not exceeded: returning response unchanged.')
                return response

            # Get and check orig_iat
            orig_iat = payload.get('orig_iat')
            if orig_iat:
                # verify expiration
                expiration_timestamp = orig_iat + int(
                    api_settings.JWT_TOKEN_RENEWAL_LIMIT.total_seconds())
                if now_timestamp > expiration_timestamp:
                    # Token has passed renew time limit - just return existing
                    # response. We need to test this process because it is
                    # probably the case that the response has already been
                    # set to an unauthorized status
                    # now_timestamp > expiration_timestamp.
                    logging.debug(
                        'JWT token has expired: returning response unchanged.')
                    return response

            else:
                # orig_iat field is required - just return existing response
                logging.debug(
                    'JWT token orig_iat field not defined: returning response unchanged.')
                return response

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            new_payload = jwt_payload_handler(user)
            new_payload['orig_iat'] = orig_iat

            # Attach the renewed token to the response
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            response['Refresh-Token'] = "JWT {0}".format(
                jwt_encode_handler(new_payload))

            logging.debug('JWT token has been renewed.')

            return response

        else:
            # No authenticated user - just return existing response
            logging.debug(
                'No JWT authenticated user: returning response unchanged.')
            return response


class AdminOnlySessionMiddleware(SessionMiddleware):
    """
    Only do the session stuff for admin urls.
    The frontend relies on auth tokens.
    """

    def process_request(self, request):
        if isAdminRequest(request):
            super(AdminOnlySessionMiddleware, self).process_request(request)
        else:
            return

    def process_response(self, request, response):
        if isAdminRequest(request):
            return super(AdminOnlySessionMiddleware, self).process_response(
                request, response)
        else:
            return response


class AdminOnlyAuthenticationMiddleware(AuthenticationMiddleware):
    """
    Only do the session authentication stuff for admin urls.
    The frontend relies on auth tokens so we clear the user.
    """

    def process_request(self, request):
        if isAdminRequest(request) and not hasattr(request, 'user'):
            super(AdminOnlyAuthenticationMiddleware, self).process_request(request)


class AdminOnlyCsrf(object):
    """
    Disable csrf for non-Admin requests, eg API
    """

    def process_request(self, request):
        if not isAdminRequest(request):
            setattr(request, '_dont_enforce_csrf_checks', True)


class LockdownMiddleware(BaseLockdownMiddleware):
    def process_request(self, request):

        common_settings = CommonPlatformSettings.load()

        if common_settings.lockdown or getattr(settings, 'FORCE_LOCKDOWN', False):
            token = request.META.get('HTTP_X_LOCKDOWN_TOKEN', None)
            if token == common_settings.token:
                return None

            url_exceptions = compile_url_exceptions(settings.LOCKDOWN_IGNORE)
            for pattern in url_exceptions:
                if pattern.search(request.path):
                    return None

            return HttpResponse('Lock-down', status=401)

        return None


authorization_logger = logging.getLogger(__name__)


class LogAuthFailureMiddleWare:
    def process_request(self, request):
        # TODO: Handle this more cleanly. The exception is raised when using IE11.
        #       Possibly related to the following issue:
        #           https://github.com/encode/django-rest-framework/issues/2774
        try:
            request.body  # touch the body so that we have access to it in process_response
        except RawPostDataException:
            pass

    def process_response(self, request, response):
        """ Log a message for each failed login attempt. """
        if reverse('admin:login') == request.path and request.method == 'POST' and response.status_code != 302:
            error = 'Authorization failed: {username} {ip}'.format(
                ip=get_client_ip(request), username=request.POST.get('username')
            )
            authorization_logger.error(error)

        if reverse('token-auth') == request.path and request.method == 'POST' and response.status_code != 200:
            try:
                data = json.loads(request.body)
            except ValueError:
                data = request.POST

            error = 'Authorization failed: {username} {ip}'.format(
                ip=get_client_ip(request), username=data.get('email')
            )
            authorization_logger.error(error)

        return response
