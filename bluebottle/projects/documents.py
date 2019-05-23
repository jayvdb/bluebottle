from django.db import connection

from django_elasticsearch_dsl import Index, DocType, fields

from bluebottle.bb_projects.models import ProjectPhase
from bluebottle.categories.models import Category
from bluebottle.donations.models import Donation
from bluebottle.geo.models import Location, Country, Place
from bluebottle.projects.models import Project, ProjectLocation
from bluebottle.tasks.models import Task, TaskMember
from bluebottle.votes.models import Vote


class MultiTenantIndex(Index):
    @property
    def _name(self):
        if connection.tenant.schema_name != 'public':
            return '{}-{}'.format(connection.tenant.schema_name, self.__name)
        return self.__name

    @_name.setter
    def _name(self, value):

        if value and value.startswith(connection.tenant.schema_name):
            value = value.replace(connection.tenant.schema_name + '-', '')

        self.__name = value


# The name of your index
project = MultiTenantIndex('projects')
# See Elasticsearch Indices API reference for available settings
project.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@project.doc_type
class ProjectDocument(DocType):
    title = fields.TextField()
    story = fields.TextField()
    pitch = fields.TextField()
    owner_id = fields.KeywordField()

    task_set = fields.NestedField(properties={
        'title': fields.TextField(),
        'description': fields.TextField(),
        'type': fields.KeywordField(),
        'status': fields.TextField(),
        'deadline': fields.DateField(),
        'deadline_to_apply': fields.DateField(),
        'location': fields.TextField(),
        'location_keyword': fields.KeywordField(attr='location'),
    })

    task_members = fields.DateField()
    people_needed = fields.IntegerField()
    donations = fields.DateField()
    votes = fields.DateField()

    status = fields.ObjectField(properties={
        'slug': fields.KeywordField(),
        'sequence': fields.ShortField(),
        'viewable': fields.BooleanField()
    })

    position = fields.GeoPointField()
    task_positions = fields.GeoPointField()

    location = fields.NestedField(properties={
        'id': fields.LongField(),
        'city': fields.TextField(),
        'name': fields.TextField()
    })

    country = fields.ObjectField(properties={
        'id': fields.LongField(),
    })

    theme = fields.LongField()

    categories = fields.NestedField(properties={
        'id': fields.LongField(),
        'slug': fields.KeywordField(),
    })

    skills = fields.LongField()

    amount_asked = fields.FloatField()
    amount_needed = fields.FloatField()

    deadline = fields.DateField()
    created = fields.DateField()
    campaign_started = fields.DateField()

    class Meta:
        model = Project
        related_models = (
            Task, TaskMember, ProjectPhase, Location, Country, Vote, Donation, Place
        )

    def get_queryset(self):
        return super(ProjectDocument, self).get_queryset().select_related(
            'location', 'country', 'theme', 'status'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Task):
            return related_instance.project
        if isinstance(related_instance, TaskMember):
            return related_instance.task.project
        elif isinstance(related_instance, ProjectPhase):
            return related_instance.project_set.all()
        elif isinstance(related_instance, Location):
            return related_instance.project_set.all()
        elif isinstance(related_instance, Country):
            return related_instance.project_set.all()
        elif isinstance(related_instance, Category):
            return related_instance.project_set.all()
        elif isinstance(related_instance, Vote):
            return related_instance.project
        elif isinstance(related_instance, Donation):
            return related_instance.project
        elif isinstance(related_instance, Place) and isinstance(related_instance.content_object, Task):
            return related_instance.content_object.project

    def prepare_position(self, instance):
        if instance.location:
            position = instance.location.position
        else:
            try:
                position = instance.projectlocation
            except ProjectLocation.DoesNotExist:
                return None

        if position and position.latitude and position.longitude:
            return {'lat': position.latitude, 'lon': position.longitude}

    def prepare_amount_asked(self, instance):
        return instance.amount_asked.amount

    def prepare_amount_needed(self, instance):
        return instance.amount_needed.amount

    def prepare_votes(self, instance):
        return [vote.created for vote in instance.vote_set.all()]

    def prepare_donations(self, instance):
        return [
            donation.created for donation
            in instance.donation_set.filter(order__status__in=('pending', 'success'))
        ]

    def prepare_task_positions(self, instance):
        return [
            {'lat': task.place.position.latitude, 'lon': task.place.position.longitude} for task
            in instance.task_set.all() if task.place and task.place.position
        ]

    def prepare_skills(self, instance):
        return [task.skill.id for task in instance.task_set.all() if task.skill]

    def prepare_theme(self, instance):
        if instance.theme:
            return instance.theme.pk

    def prepare_task_members(self, instance):
        result = []
        for task in instance.task_set.all():
            result += [
                member.created for member in task.members.all()
            ]

        return result