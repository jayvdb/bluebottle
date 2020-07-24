from django.utils.translation import ugettext_lazy as _

from bluebottle.fsm.effects import Effect
from bluebottle.follow.models import follow, unfollow


class FollowActivityEffect(Effect):
    "Follow activity"

    post_save = True

    def execute(self, **kwargs):
        if self.instance.user:
            follow(self.instance.user, self.instance.activity)

    def __repr__(self):
        return '<Effect: Follow {} by {}>'.format(self.instance.activity, self.instance.user)

    def __unicode__(self):
        user = self.instance.user
        if not self.instance.user.id:
            user = self.instance.user.full_name
        return _('{user} will receive updates for {activity}.').format(activity=self.instance.activity, user=user)


class UnFollowActivityEffect(Effect):
    "Unfollow activity"

    post_save = True

    def execute(self, **kwargs):
        if self.instance.user:
            unfollow(self.instance.user, self.instance.activity)

    def __repr__(self):
        return '<Effect: Unfollow {} by {}>'.format(self.instance.activity, self.instance.user)

    def __unicode__(self):
        user = self.instance.user
        if not self.instance.user.id:
            user = self.instance.user.full_name
        return _('{user} will no longer receive updates for {activity}.').format(activity=self.instance.activity, user=user)
