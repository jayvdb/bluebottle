import importlib

from bluebottle.projects.dashboard import RecentProjects, MyReviewingProjects, ClosingFundingProjects
from django.urls.base import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, DefaultAppIndexDashboard
from jet.dashboard.modules import DashboardModule

from bluebottle.tasks.models import Task


class ClosingTasks(DashboardModule):
    title = _('Tasks nearing deadline')
    title_url = reverse('admin:tasks_task_changelist')
    template = 'dashboard/closing_tasks.html'
    limit = 5

    def init_with_context(self, context):
        tasks = Task.objects.exclude(deadline__lt=now()).filter(status__in=['open', 'full']).order_by('deadline')
        self.children = tasks[:self.limit]


class CustomIndexDashboard(Dashboard):
    columns = 2

    class Media:
        css = ('css/admin/dashboard.css', )

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.children.append(RecentProjects())
        self.children.append(MyReviewingProjects())
        self.children.append(ClosingFundingProjects())
        self.children.append(ClosingTasks())


class CustomAppIndexDashboard(DefaultAppIndexDashboard):

    def __new__(cls, context, **kwargs):
        try:
            mod = importlib.import_module("bluebottle.{}.dashboard".format(kwargs['app_label']))
            dash = mod.AppIndexDashboard(context, **kwargs)
            return dash
        except ImportError:
            return DefaultAppIndexDashboard(context, **kwargs)
