from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework_json_api.relations import ResourceRelatedField

from bluebottle.activities.utils import (
    BaseActivitySerializer, BaseContributionSerializer,
    ActivityValidationSerializer
)
from bluebottle.assignments.filters import ApplicantListFilter
from bluebottle.assignments.models import Assignment, Applicant
from bluebottle.events.serializers import LocationValidator, LocationField
from bluebottle.geo.models import Geolocation
from bluebottle.transitions.serializers import TransitionSerializer
from bluebottle.utils.serializers import RelatedField, ResourcePermissionField, NonModelRelatedResourceField, \
    FilteredRelatedField


class RegistrationDeadlineValidator(object):
    def set_context(self, field):
        self.end_date = field.parent.instance.end_date

    def __call__(self, value):
        if not self.end_date or value > self.end_date:
            raise serializers.ValidationError(
                _('Registration deadline should be before end date'),
                code='registration_deadline'
            )

        return value


class AssignmentValidationSerializer(ActivityValidationSerializer):
    end_date = serializers.DateField()
    duration = serializers.FloatField()
    registration_deadline = serializers.DateField(
        allow_null=True,
        validators=[RegistrationDeadlineValidator()]
    )
    is_online = serializers.BooleanField()
    end_date_type = serializers.CharField()
    location = LocationField(
        queryset=Geolocation.objects.all(),
        allow_null=True,
        validators=[LocationValidator()]
    )

    class Meta:
        model = Assignment
        fields = ActivityValidationSerializer.Meta.fields + (
            'end_date', 'end_date_type',
            'is_online', 'location', 'duration',
            'registration_deadline',
        )

    class JSONAPIMeta:
        resource_name = 'activities/assignment-validations'


class AssignmentListSerializer(BaseActivitySerializer):
    permissions = ResourcePermissionField('assignment-detail', view_args=('pk',))
    validations = NonModelRelatedResourceField(AssignmentValidationSerializer)

    class Meta(BaseActivitySerializer.Meta):
        model = Assignment
        fields = BaseActivitySerializer.Meta.fields + (
            'is_online',
            'end_date',
            'end_date_type',
            'registration_deadline',
            'capacity',
            'expertise',
            'duration',
            'location',
            'permissions',
            'validations'
        )

    class JSONAPIMeta(BaseActivitySerializer.JSONAPIMeta):
        included_resources = [
            'owner',
            'location',
            'initiative',
            'initiative.image',
            'initiative.location',
            'initiative.place',
            'validations',
        ]
        resource_name = 'activities/assignments'

    included_serializers = {
        'owner': 'bluebottle.initiatives.serializers.MemberSerializer',
        'initiative': 'bluebottle.initiatives.serializers.InitiativeSerializer',
        'initiative.image': 'bluebottle.initiatives.serializers.InitiativeImageSerializer',
        'location': 'bluebottle.geo.serializers.GeolocationSerializer',
        'validations': 'bluebottle.assignments.serializers.AssignmentValidationSerializer',
    }


class AssignmentSerializer(AssignmentListSerializer):
    contributions = FilteredRelatedField(many=True, filter_backend=ApplicantListFilter)
    location = RelatedField(allow_null=True, required=False, queryset=Geolocation.objects.all())

    class Meta(AssignmentListSerializer.Meta):
        fields = AssignmentListSerializer.Meta.fields + (
            'contributions',
        )

    class JSONAPIMeta(AssignmentListSerializer.JSONAPIMeta):
        included_resources = AssignmentListSerializer.JSONAPIMeta.included_resources + [
            'contributions',
            'contributions.user'
        ]

    included_serializers = dict(
        AssignmentListSerializer.included_serializers,
        **{
            'contributions': 'bluebottle.funding.serializers.DonationSerializer',
        }
    )


class AssignmentTransitionSerializer(TransitionSerializer):
    resource = ResourceRelatedField(queryset=Assignment.objects.all())
    field = 'transitions'
    included_serializers = {
        'resource': 'bluebottle.assignments.serializers.AssignmentSerializer',
    }

    class JSONAPIMeta:
        included_resources = ['resource', ]
        resource_name = 'assignment-transitions'


class ApplicantSerializer(BaseContributionSerializer):

    class Meta(BaseContributionSerializer.Meta):
        model = Applicant
        fields = BaseContributionSerializer.Meta.fields + ('time_spent', )


class ApplicantTransitionSerializer(TransitionSerializer):
    resource = ResourceRelatedField(queryset=Applicant.objects.all())
    field = 'transitions'
    included_serializers = {
        'resource': 'bluebottle.assignments.serializers.ApplicantSerializer',
        'resource.activity': 'bluebottle.assignments.serializers.AssignmentSerializer',
    }

    class JSONAPIMeta:
        resource_name = 'contributions/applicant-transitions'
        included_resources = [
            'resource',
            'resource.activity'
        ]
