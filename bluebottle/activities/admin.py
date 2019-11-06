from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from polymorphic.admin import (
    PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter,
    StackedPolymorphicInline)

from bluebottle.activities.models import Activity, Contribution
from bluebottle.events.models import Event, Participant
from bluebottle.follow.admin import FollowAdminInline
from bluebottle.funding.models import Funding, Donation
from bluebottle.assignments.models import Assignment, Applicant
from bluebottle.utils.admin import FSMAdmin


class ContributionChildAdmin(PolymorphicChildModelAdmin, FSMAdmin):
    base_model = Contribution
    search_fields = ['user__first_name', 'user__last_name', 'activity__title']
    list_filter = ['status', ]
    ordering = ('-created', )
    show_in_index = True

    def activity_link(self, obj):
        url = reverse("admin:{}_{}_change".format(
            obj.activity._meta.app_label,
            obj.activity._meta.model_name),
            args=(obj.activity.id,)
        )
        return format_html(u"<a href='{}'>{}</a>", url, obj.activity.title or '-empty-')
    activity_link.short_description = _('Activity')


@admin.register(Contribution)
class ContributionAdmin(PolymorphicParentModelAdmin, FSMAdmin):
    base_model = Contribution
    child_models = (Participant, Donation, Applicant)
    list_display = ['created', 'owner', 'type', 'activity', 'status']
    list_filter = (PolymorphicChildModelFilter, 'status')

    ordering = ('-created', )

    def type(self, obj):
        return obj.get_real_instance_class().__name__


class ActivityChildAdmin(PolymorphicChildModelAdmin, FSMAdmin):
    base_model = Activity
    raw_id_fields = ['owner', 'initiative']
    inlines = (FollowAdminInline,)
    show_in_index = True

    ordering = ('-created', )

    readonly_fields = [
        'created',
        'updated',
        'status',
        'review_status',
        'valid',
        'complete',
        'transition_date',
        'stats_data']

    basic_fields = (
        'title',
        'slug',
        'initiative',
        'owner',
        'created',
        'updated',
        'stats_data',
    )

    def get_status_fields(self, request, obj=None):
        if obj and obj.status == 'in_review':
            return [
                'title',
                'complete',
                'valid',
                'review_status',
                'review_transitions',
                'transition_date'
            ]
        return [
            'complete',
            'valid',
            'status',
            'transitions',
            'transition_date'
        ]

    status_fields = (
        'complete',
        'valid',
        'status',
        'transitions',
        'transition_date'
    )

    detail_fields = (
        'description',
        'highlight'
    )

    def get_fieldsets(self, request, obj=None):
        return (
            (_('Basic'), {'fields': self.basic_fields}),
            (_('Details'), {'fields': self.detail_fields}),
            (_('Status'), {'fields': self.get_status_fields(request, obj)}),
        )

    def stats_data(self, obj):
        return format_html("<table>{}</table>", format_html("".join([
            format_html(u"<tr><th>{}</th><td>{}</td></tr>", key, value) for key, value in obj.stats.items()
        ])))

    stats_data.short_description = _('Statistics')

    def valid(self, obj):
        if not obj.review_transitions.is_valid():
            return '-'
        return format_html("<ul>{}</ul>", format_html("".join([
            format_html(u"<li>{}</li>", value) for value in obj.review_transitions.is_valid()
        ])))

    valid.short_description = _('Validation errors')

    def complete(self, obj):
        if not obj.review_transitions.is_complete():
            return '-'
        return format_html("<ul>{}</ul>", format_html("".join([
            format_html(u"<li>{}</li>", value) for value in obj.review_transitions.is_complete()
        ])))

    complete.short_description = _('Missing data')


@admin.register(Activity)
class ActivityAdmin(PolymorphicParentModelAdmin, FSMAdmin):
    base_model = Activity
    child_models = (Event, Funding, Assignment)
    readonly_fields = ['link']
    list_filter = (PolymorphicChildModelFilter, 'status', 'review_status', 'highlight')
    list_editable = ('highlight',)

    list_display = ['__unicode__', 'created', 'type', 'status', 'review_status',
                    'link', 'highlight']

    search_fields = ('title', 'description', 'owner__first_name', 'owner__last_name')

    def link(self, obj):
        return format_html(u'<a href="{}" target="_blank">{}</a>', obj.get_absolute_url(), obj.title)

    link.short_description = _("Show on site")

    ordering = ('-created', )

    def type(self, obj):
        return obj.get_real_instance_class().__name__


class ActivityAdminInline(StackedPolymorphicInline):
    model = Activity
    readonly_fields = ['title', 'created', 'status', 'owner']
    fields = readonly_fields
    extra = 0
    can_delete = False

    class ActivityLinkMixin(object):
        def activity_link(self, obj):
            url = reverse("admin:{}_{}_change".format(
                obj._meta.app_label,
                obj._meta.model_name),
                args=(obj.id,)
            )
            return format_html("<a href='{}'>{}</a>", url, obj.title or '-empty-')

        activity_link.short_description = _('Edit activity')

        def link(self, obj):
            return format_html('<a href="{}" target="_blank">{}</a>', obj.get_absolute_url(), obj.title or '-empty-')

        link.short_description = _('View on site')

    class EventInline(StackedPolymorphicInline.Child, ActivityLinkMixin):
        readonly_fields = ['activity_link', 'link', 'start_date', 'start_time', 'duration', 'status']
        fields = readonly_fields
        model = Event

    class FundingInline(StackedPolymorphicInline.Child, ActivityLinkMixin):
        readonly_fields = ['activity_link', 'link', 'target', 'deadline', 'status']
        fields = readonly_fields
        model = Funding

    class AssignmentInline(StackedPolymorphicInline.Child, ActivityLinkMixin):
        readonly_fields = ['activity_link', 'link', 'end_date', 'duration', 'status']
        fields = readonly_fields
        model = Assignment

    child_inlines = (
        EventInline,
        FundingInline,
        AssignmentInline
    )