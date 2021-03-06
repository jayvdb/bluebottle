from django.urls.base import reverse
from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import DefaultAppIndexDashboard
from jet.dashboard.modules import DashboardModule

from bluebottle.events.models import Event


class RecentEvents(DashboardModule):
    title = _('Recently submitted events')
    title_url = "{}?status[]=draft&status[]=open".format(reverse('admin:events_event_changelist'))
    template = 'dashboard/recent_events.html'
    limit = 5
    column = 0

    def init_with_context(self, context):
        activities = Event.objects.filter(status__in=['draft', 'open']).order_by('-created')
        self.children = activities[:self.limit]


class AppIndexDashboard(DefaultAppIndexDashboard):

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.children.append(RecentEvents())
