from html.parser import HTMLParser
from urllib.parse import urlencode

from django.db import models, connection
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from djchoices.choices import DjangoChoices, ChoiceItem

from bluebottle.activities.models import Activity, Contributor, Contribution
from bluebottle.files.fields import PrivateDocumentField
from bluebottle.geo.models import Geolocation


class TimeBasedActivity(Activity):
    capacity = models.PositiveIntegerField(_('attendee limit'), null=True, blank=True)

    is_online = models.NullBooleanField(_('is online'), null=True, default=None)
    location = models.ForeignKey(Geolocation, verbose_name=_('location'),
                                 null=True, blank=True, on_delete=models.SET_NULL)
    location_hint = models.TextField(_('location hint'), null=True, blank=True)

    registration_deadline = models.DateField(_('deadline to apply'), null=True, blank=True)

    expertise = models.ForeignKey('tasks.Skill', verbose_name=_('skill'), blank=True, null=True)

    review = models.NullBooleanField(_('review participants'), null=True, default=None)

    @property
    def required_fields(self):
        fields = ['title', 'description', 'is_online', 'review', ]

        if not self.is_online:
            fields.append('location')

        return fields

    @property
    def participants(self):
        return self.contributors.instance_of(PeriodParticipant, DateParticipant)

    @property
    def active_participants(self):
        return self.participants.filter(status__in=('accepted', 'new',))

    @property
    def accepted_participants(self):
        return self.participants.filter(status='accepted')

    @property
    def durations(self):
        return TimeContribution.objects.filter(
            contributor__activity=self
        )

    @property
    def accepted_durations(self):
        return self.durations.filter(
            contributor__status='accepted'
        )

    @property
    def values(self):
        return TimeContribution.objects.filter(
            contributor__activity=self,
            status='succeeded'
        )


class DateActivity(TimeBasedActivity):
    start = models.DateTimeField(_('activity date'), null=True, blank=True)
    duration = models.DurationField(_('duration'), null=True, blank=True)

    online_meeting_url = models.TextField(_('Online Meeting URL'), blank=True, default='')

    duration_period = 'overall'

    class Meta:
        verbose_name = _("Activity on a date")
        verbose_name_plural = _("Activities on a date")
        permissions = (
            ('api_read_dateactivity', 'Can view on a date activities through the API'),
            ('api_add_dateactivity', 'Can add on a date activities through the API'),
            ('api_change_dateactivity', 'Can change on a date activities through the API'),
            ('api_delete_dateactivity', 'Can delete on a date activities through the API'),

            ('api_read_own_dateactivity', 'Can view own on a date activities through the API'),
            ('api_add_own_dateactivity', 'Can add own on a date activities through the API'),
            ('api_change_own_dateactivity', 'Can change own on a date activities through the API'),
            ('api_delete_own_dateactivity', 'Can delete own on a date activities through the API'),
        )

    class JSONAPIMeta:
        resource_name = 'activities/time-based/dates'

    @property
    def activity_date(self):
        return self.start

    @property
    def required_fields(self):
        fields = super().required_fields

        return fields + ['start', 'duration']

    @property
    def uid(self):
        return '{}-{}-{}'.format(connection.tenant.client_name, 'dateactivity', self.pk)

    @property
    def google_calendar_link(self):
        def format_date(date):
            if date:
                return date.astimezone(timezone.utc).strftime('%Y%m%dT%H%M%SZ')

        url = u'https://calendar.google.com/calendar/render'
        params = {
            'action': u'TEMPLATE',
            'text': self.title,
            'dates': u'{}/{}'.format(
                format_date(self.start), format_date(self.start + self.duration)
            ),
            'details': HTMLParser().unescape(
                u'{}\n{}'.format(
                    strip_tags(self.description), self.get_absolute_url()
                )
            ),
            'uid': self.uid,
        }

        if self.location:
            params['location'] = self.location.formatted_address

        return u'{}?{}'.format(url, urlencode(params))

    @property
    def outlook_link(self):
        def format_date(date):
            if date:
                return date.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')

        url = 'https://outlook.live.com/owa/'

        params = {
            'rru': 'addevent',
            'path': '/calendar/action/compose&rru=addevent',
            'allday': False,
            'subject': self.title,
            'startdt': format_date(self.start),
            'enddt': format_date(self.start + self.duration),
            'body': HTMLParser().unescape(
                u'{}\n{}'.format(
                    strip_tags(self.description), self.get_absolute_url()
                )
            ),
        }

        if self.location:
            params['location'] = self.location.formatted_address

        return u'{}?{}'.format(url, urlencode(params))


class DurationPeriodChoices(DjangoChoices):
    overall = ChoiceItem('overall', label=_("overall"))
    days = ChoiceItem('days', label=_("per day"))
    weeks = ChoiceItem('weeks', label=_("per week"))
    months = ChoiceItem('months', label=_("per month"))


class PeriodActivity(TimeBasedActivity):
    start = models.DateField(_('start'), null=True, blank=True)
    deadline = models.DateField(_('deadline'), null=True, blank=True)

    duration = models.DurationField(_('duration'), null=True, blank=True)
    duration_period = models.CharField(
        _('duration period'),
        max_length=20,
        blank=True,
        null=True,
        choices=DurationPeriodChoices.choices,
    )

    @property
    def activity_date(self):
        return self.deadline or self.start

    class Meta:
        verbose_name = _("Activity during a period")
        verbose_name_plural = _("Activities during a period")
        permissions = (
            ('api_read_periodactivity', 'Can view during a period activities through the API'),
            ('api_add_periodactivity', 'Can add during a period activities through the API'),
            ('api_change_periodactivity', 'Can change during a period activities through the API'),
            ('api_delete_periodactivity', 'Can delete during a period activities through the API'),

            ('api_read_own_periodactivity', 'Can view own during a period activities through the API'),
            ('api_add_own_periodactivity', 'Can add own during a period activities through the API'),
            ('api_change_own_periodactivity', 'Can change own during a period activities through the API'),
            ('api_delete_own_periodactivity', 'Can delete own during a period activities through the API'),
        )

    class JSONAPIMeta:
        resource_name = 'activities/time-based/periods'

    @property
    def required_fields(self):
        fields = super().required_fields

        return fields + ['deadline', 'duration', 'duration_period']


class Participant(Contributor):
    def __str__(self):
        return self.user

    @property
    def finished_contributions(self):
        return self.contribution_values.filter(
            timecontribution__end__lte=timezone.now()
        )

    class Meta:
        abstract = True


class DateParticipant(Participant):
    motivation = models.TextField(blank=True, null=True)
    document = PrivateDocumentField(blank=True, null=True)

    class Meta(object):
        verbose_name = _("Participant on a date")
        verbose_name_plural = _("Participants on a date")
        permissions = (
            ('api_read_dateparticipant', 'Can view participant through the API'),
            ('api_add_dateparticipant', 'Can add participant through the API'),
            ('api_change_dateparticipant', 'Can change participant through the API'),
            ('api_delete_dateparticipant', 'Can delete participant through the API'),

            ('api_read_own_dateparticipant', 'Can view own participant through the API'),
            ('api_add_own_dateparticipant', 'Can add own participant through the API'),
            ('api_change_own_dateparticipant', 'Can change own participant through the API'),
            ('api_delete_own_dateparticipant', 'Can delete own participant through the API'),
        )

    class JSONAPIMeta:
        resource_name = 'contributors/time-based/date-participants'

    def __str__(self):
        return _("Participant {name}").format(name=self.user)


class PeriodParticipant(Participant, Contributor):
    motivation = models.TextField(blank=True, null=True)
    document = PrivateDocumentField(blank=True, null=True)

    current_period = models.DateField(null=True, blank=True)

    class Meta(object):
        verbose_name = _("Participant during a period")
        verbose_name_plural = _("Participants during a period")
        permissions = (
            ('api_read_periodparticipant', 'Can view period participant through the API'),
            ('api_add_periodparticipant', 'Can add period participant through the API'),
            ('api_change_periodparticipant', 'Can change period participant through the API'),
            ('api_delete_periodparticipant', 'Can delete period participant through the API'),

            ('api_read_own_periodparticipant', 'Can view own period participant through the API'),
            ('api_add_own_periodparticipant', 'Can add own participant through the API'),
            ('api_change_own_periodparticipant', 'Can change own period participant through the API'),
            ('api_delete_own_periodparticipant', 'Can delete own period participant through the API'),
        )

    @property
    def current_contribution(self):
        return self.contribution_values.get(status='new')

    def __str__(self):
        return _("Participant {name}").format(name=self.user)

    class JSONAPIMeta:
        resource_name = 'contributors/time-based/period-participants'


class TimeContribution(Contribution):
    value = models.DurationField(_('value'))
    start = models.DateTimeField(_('start'))
    end = models.DateTimeField(_('end'), null=True, blank=True)

    class Meta:
        verbose_name = _("Contribution")
        verbose_name_plural = _("Contributions")

    def __str__(self):
        return _("Session {name} {date}").format(
            name=self.contributor.user,
            date=self.start.date()
        )


from bluebottle.time_based.periodic_tasks import *  # noqa
