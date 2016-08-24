import re
from django.utils.translation import ugettext as _

from rest_framework import serializers
from bs4 import BeautifulSoup
from localflavor.generic.validators import IBANValidator

from bluebottle.bb_projects.models import ProjectTheme, ProjectPhase
from bluebottle.bluebottle_drf2.serializers import (
    OEmbedField, SorlImageField, ImageSerializer,
    PrivateFileSerializer
)
from bluebottle.donations.models import Donation
from bluebottle.geo.models import Country, Location
from bluebottle.geo.serializers import CountrySerializer
from bluebottle.categories.models import Category
from bluebottle.utils.serializers import MoneySerializer
from bluebottle.members.serializers import UserProfileSerializer, UserPreviewSerializer
from bluebottle.projects.models import ProjectBudgetLine, ProjectDocument, Project
from bluebottle.tasks.models import TaskMember
from bluebottle.wallposts.models import MediaWallpostPhoto, MediaWallpost, TextWallpost


class ProjectPhaseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPhase


class ProjectPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPhase


class ProjectThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTheme
        fields = ('id', 'name', 'description')


class StoryField(serializers.CharField):
    def to_representation(self, value):
        """ Reading / Loading the story field """
        return value

    def to_internal_value(self, data):
        """
        Saving the story text

        Convert &gt; and &lt; back to HTML tags so Beautiful Soup can clean
        unwanted tags. Script tags are sent by redactor as
        "&lt;;script&gt;;", Iframe tags have just one semicolon.
        """
        data = data.replace("&lt;;", "<").replace("&gt;;", ">")
        data = data.replace("&lt;", "<").replace("&gt;", ">")
        soup = BeautifulSoup(data, "html.parser")
        [s.extract() for s in soup(['script', 'iframe'])]
        return unicode(soup)


class ProjectCountrySerializer(CountrySerializer):
    subregion = serializers.CharField(source='subregion.name')

    class Meta:
        model = Country
        fields = ('id', 'name', 'subregion', 'code')


class ProjectBudgetLineSerializer(serializers.ModelSerializer):
    amount = MoneySerializer()
    project = serializers.SlugRelatedField(slug_field='slug', queryset=Project.objects)

    class Meta:
        model = ProjectBudgetLine
        fields = ('id', 'project', 'description', 'amount')


class BasicProjectBudgetLineSerializer(serializers.ModelSerializer):
    amount = MoneySerializer()

    class Meta:
        model = ProjectBudgetLine
        fields = ('description', 'amount')


class ProjectDocumentSerializer(serializers.ModelSerializer):
    file = PrivateFileSerializer()
    project = serializers.SlugRelatedField(slug_field='slug', queryset=Project.objects)

    class Meta:
        model = ProjectDocument
        fields = ('id', 'project', 'file')


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='slug', read_only=True)
    owner = UserProfileSerializer()
    image = ImageSerializer(required=False)
    task_count = serializers.IntegerField()
    country = ProjectCountrySerializer()
    story = StoryField()
    is_funding = serializers.ReadOnlyField()
    budget_lines = BasicProjectBudgetLineSerializer(
        many=True, source='projectbudgetline_set', read_only=True)
    video_html = OEmbedField(source='video_url', maxwidth='560',
                             maxheight='315')
    location = serializers.PrimaryKeyRelatedField(required=False, queryset=Location.objects)
    vote_count = serializers.IntegerField()
    supporter_count = serializers.IntegerField()

    people_requested = serializers.ReadOnlyField()
    people_registered = serializers.ReadOnlyField()

    amount_asked = MoneySerializer()
    amount_donated = MoneySerializer()
    amount_needed = MoneySerializer()
    amount_extra = MoneySerializer()

    categories = serializers.SlugRelatedField(slug_field='slug', many=True,
                                              queryset=Category.objects)

    def __init__(self, *args, **kwargs):
        super(ProjectSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = ('id', 'created', 'title', 'pitch', 'organization',
                  'description', 'owner', 'status', 'image',
                  'country', 'theme', 'categories', 'language',
                  'latitude', 'longitude', 'amount_asked', 'amount_donated',
                  'amount_needed', 'amount_extra', 'allow_overfunding',
                  'task_count', 'amount_asked', 'amount_donated',
                  'amount_needed', 'amount_extra', 'story', 'budget_lines',
                  'status', 'deadline', 'is_funding', 'vote_count',
                  'supporter_count', 'people_requested', 'people_registered',
                  'voting_deadline', 'latitude', 'longitude', 'video_url',
                  'video_html', 'location', 'project_type')


class ProjectPreviewSerializer(ProjectSerializer):
    image = ImageSerializer(required=False)
    theme = ProjectThemeSerializer()

    owner = UserPreviewSerializer()

    categories = serializers.SlugRelatedField(many=True, read_only=True,
                                              slug_field='slug')

    class Meta:
        model = Project
        fields = ('id', 'title', 'status', 'image', 'country', 'pitch',
                  'theme', 'categories', 'owner', 'amount_asked', 'amount_donated',
                  'amount_needed', 'amount_extra', 'deadline', 'latitude',
                  'longitude', 'task_count', 'allow_overfunding', 'is_campaign',
                  'is_funding', 'people_requested',
                  'people_registered', 'location', 'vote_count',
                  'voting_deadline', 'project_type')


class ProjectTinyPreviewSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    image = SorlImageField('400x300', crop='center')

    class Meta:
        model = Project
        fields = ('id', 'title', 'slug', 'status', 'image', 'latitude', 'longitude')


class ManageProjectSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='slug', read_only=True)

    url = serializers.HyperlinkedIdentityField(
        view_name='project_manage_detail', lookup_field='slug')

    editable = serializers.BooleanField(read_only=True)
    viewable = serializers.BooleanField(read_only=True)
    status = serializers.PrimaryKeyRelatedField(required=False, allow_null=True,
                                                queryset=ProjectPhase.objects)
    location = serializers.PrimaryKeyRelatedField(required=False, allow_null=True,
                                                  queryset=Location.objects)
    image = ImageSerializer(required=False, allow_null=True)
    pitch = serializers.CharField(required=False, allow_null=True)
    slug = serializers.CharField(read_only=True)

    amount_asked = MoneySerializer(required=False, allow_null=True)
    amount_donated = MoneySerializer(read_only=True)
    amount_needed = MoneySerializer(read_only=True)

    budget_lines = ProjectBudgetLineSerializer(many=True,
                                               source='projectbudgetline_set',
                                               read_only=True)
    video_html = OEmbedField(source='video_url', maxwidth='560',
                             maxheight='315')
    story = StoryField(required=False, allow_blank=True)
    is_funding = serializers.ReadOnlyField()

    documents = ProjectDocumentSerializer(
        many=True, read_only=True)

    def validate_account_number(self, value):

        if value:
            country_code = value[:2]
            digits_regex = re.compile('\d{2}')
            check_digits = value[2:4]

            # Only try iban validaton when the field matches start of
            # iban format as the field can also contain non-iban
            # account numbers.
            # Expecting something like: NL18xxxxxxxxxx
            iban_validator = IBANValidator()
            if country_code in iban_validator.validation_countries.keys() and \
               digits_regex.match(check_digits):
                iban_validator(value)
        return value

    def validate_status(self, value):
        if not value:
            value = ProjectPhase.objects.order_by('sequence').all()[0]
        else:
            """
            Don't let the owner set a status with a sequence number higher
            than 2
            They can set 1: plan-new or 2: plan-submitted

            TODO: This needs work. Maybe we could use a FSM for the project
                  status
                  transitions, e.g.:
                      https://pypi.python.org/pypi/django-fsm/1.2.0

            TODO: what to do if the expected status (plan-submitted) is
                  not found?! Hard fail?
            """
            submit_status = ProjectPhase.objects.get(slug='plan-submitted')
            new_status = ProjectPhase.objects.get(slug='plan-new')
            needs_work_status = ProjectPhase.objects.get(
                slug='plan-needs-work')

            proposed_status = value
            current_status = None

            # Get the current status or the first if not found
            try:
                current_status = Project.objects.get(slug=self.initial_data['slug']).status
            except (Project.DoesNotExist, KeyError):
                current_status = ProjectPhase.objects.order_by(
                    'sequence').all()[0]

            if current_status and proposed_status:
                """
                These are possible combinations of current v. proposed status
                which are permitted:
                1) the current status is the same as the proposed status
                2) the current is new or needs work and the proposed
                   is submitted
                """
                if proposed_status == current_status:
                    return value
                if proposed_status != submit_status or current_status not in [new_status, needs_work_status]:
                    raise serializers.ValidationError(_("You can not change the project state."))
        return value

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'editable', 'viewable',
                  'status', 'image', 'pitch', 'slug', 'created',
                  'url', 'country', 'location', 'place', 'theme', 'categories',
                  'organization', 'language', 'account_holder_name',
                  'account_holder_address', 'account_holder_postal_code',
                  'account_holder_city', 'account_holder_country',
                  'account_number', 'account_bic', 'documents',
                  'account_bank_country', 'amount_asked',
                  'amount_donated', 'amount_needed', 'video_url',
                  'video_html', 'is_funding', 'story',
                  'budget_lines', 'deadline', 'latitude', 'longitude',
                  'project_type')


class ProjectDonationSerializer(serializers.ModelSerializer):
    member = UserPreviewSerializer(source='user')
    date_donated = serializers.DateTimeField(source='ready')
    amount = MoneySerializer()

    class Meta:
        model = Donation
        fields = ('member', 'date_donated', 'amount',)


class ProjectWallpostPhotoSerializer(serializers.ModelSerializer):
    photo = ImageSerializer()
    created = serializers.DateTimeField(source='mediawallpost.created')

    class Meta:
        model = MediaWallpostPhoto
        fields = ('id', 'photo', 'created')


class ProjectWallpostVideoSerializer(serializers.ModelSerializer):
    video_html = OEmbedField(source='video_url', maxwidth='560', maxheight='315')
    video_url = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = MediaWallpost
        fields = ('id', 'video_url', 'video_html', 'created')


class ProjectMediaSerializer(serializers.ModelSerializer):
    pictures = ProjectWallpostPhotoSerializer(source='wallpost_photos', many=True)
    videos = ProjectWallpostVideoSerializer(source='wallpost_videos', many=True)
    id = serializers.CharField(source='slug')

    class Meta:
        model = Project
        fields = ('id', 'title', 'pictures', 'videos')


class ProjectDonorSerializer(serializers.ModelSerializer):
    """
    Members that made a donation
    """
    user = UserPreviewSerializer()

    class Meta:
        model = Donation
        fields = ('id', 'user', 'created')


class ProjectTaskMemberSerializer(serializers.ModelSerializer):
    """
    Members that joined a task
    """
    user = UserPreviewSerializer(source='member')

    class Meta:
        model = TaskMember
        fields = ('id', 'user', 'created', 'motivation', 'task')


class ProjectPosterSerializer(serializers.ModelSerializer):
    """
    Members that wrote a wallpost
    """
    user = UserPreviewSerializer(source='author')

    class Meta:
        model = TextWallpost
        fields = ('id', 'user', 'created', 'text')


class ProjectSupportSerializer(serializers.ModelSerializer):
    """
    Lists with different project supporter types
    """

    donors = ProjectDonorSerializer(many=True)
    task_members = ProjectTaskMemberSerializer(many=True)
    posters = ProjectPosterSerializer(many=True)
    id = serializers.CharField(source='slug')

    class Meta:
        model = Project
        fields = ('id', 'title', 'donors', 'task_members', 'posters')
