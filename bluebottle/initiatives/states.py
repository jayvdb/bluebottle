from django.utils.translation import ugettext_lazy as _

from bluebottle.fsm.effects import RelatedTransitionEffect
from bluebottle.fsm.state import ModelStateMachine, State, EmptyState, Transition
from bluebottle.initiatives.effects import (
    ApproveActivities, RejectActivities, CancelActivities, DeleteActivities
)
from bluebottle.initiatives.messages import InitiativeRejectedOwnerMessage, InitiativeApprovedOwnerMessage, \
    InitiativeCancelledOwnerMessage
from bluebottle.initiatives.models import Initiative
from bluebottle.notifications.effects import NotificationEffect


class ReviewStateMachine(ModelStateMachine):
    field = 'status'
    model = Initiative

    draft = State(
        _('draft'),
        'draft',
        _('The initiative has been created and is being worked on.')
    )
    submitted = State(
        _('submitted'),
        'submitted',
        _('The initiative has been submitted and is ready to be reviewed.')
    )
    needs_work = State(
        _('needs work'),
        'needs_work',
        _('The initiative has been submitted but needs adjustments in order to be approved.')
    )
    rejected = State(
        _('rejected'),
        'rejected',
        _("The initiative doesn't fit the program or the rules of the game. "
          "The initiative is not visible in the frontend, but does count in the reporting. "
          "The initiative cannot be edited by the initiator.")
    )
    cancelled = State(
        _('cancelled'),
        'cancelled',
        _('The initiative is not executed. '
          'The initiative is not visible in the frontend, but does count in the reporting. '
          'The initiative cannot be edited by the initiator.')
    )
    deleted = State(
        _('deleted'),
        'deleted',
        _('The initiative is not visible in the frontend and does not count in the reporting. '
          'The initiative cannot be edited by the initiator.')
    )
    approved = State(
        _('approved'),
        'approved',
        _('The initiative is visible in the frontend and complete activities are open for contributions.')
    )

    def is_complete(self):
        """The initiative is complete"""
        if self.instance.organization and list(self.instance.organization.required):
            return False

        if self.instance.organization_contact and list(self.instance.organization_contact.required):
            return False

        return not list(self.instance.required)

    def is_valid(self):
        """The initiative is valid"""
        if self.instance.organization and list(self.instance.organization.errors):
            return False

        if self.instance.organization_contact and list(self.instance.organization_contact.errors):
            return False

        return not list(self.instance.errors)

    def is_staff(self, user):
        return user.is_staff

    initiate = Transition(EmptyState(), draft)

    submit = Transition(
        [draft, needs_work],
        submitted,
        name=_('Submit'),
        description=_("The initiative will be submitted for review."),
        conditions=[is_complete, is_valid],
        automatic=False,
        effects=[
            RelatedTransitionEffect('activities', 'submit')
        ]
    )

    approve = Transition(
        submitted,
        approved,
        name=_('Approve'),
        description=_("The initiative will be visible in the frontend and "
                      "complete activities will be open for contributions."),
        conditions=[is_complete, is_valid],
        automatic=False,
        permission=is_staff,
        effects=[
            ApproveActivities,
            NotificationEffect(InitiativeApprovedOwnerMessage)
        ]
    )

    request_changes = Transition(
        submitted,
        needs_work,
        name=_('Needs work'),
        description=_("The status of the initiative is set to 'Needs work'. "
                      "The initiator can edit and resubmit the initiative. "
                      "Don't forget to inform the initiator of the necessary adjustments."),
        conditions=[],
        automatic=False,
    )

    reject = Transition(
        [
            draft,
            submitted,
            needs_work,
            approved,
            cancelled
        ],
        rejected,
        name=_('Reject'),
        description=_("Reject in case this initiative doesn't fit your program or the rules of the game. "
                      "The initiator will not be able to edit the initiative and it won't be visible on the front end. "
                      "The initiative will still be available in the back office and appear in your reporting. "
                      "The initiator will not be able to edit it and it won't be visible on the platform."),
        automatic=False,
        permission=is_staff,
        effects=[
            RejectActivities,
            NotificationEffect(InitiativeRejectedOwnerMessage)
        ]
    )

    cancel = Transition(
        approved,
        cancelled,
        name=_('Cancel'),
        description=_("Cancel if the initiative will not be executed. "
                      "The initiator will not be able to edit the initiative and it won't be visible on the front end. "
                      "The initiative will still be available in the back office and appear in your reporting."),
        automatic=False,
        effects=[
            CancelActivities,
            NotificationEffect(InitiativeCancelledOwnerMessage)
        ]
    )

    delete = Transition(
        [
            draft,
            rejected,
            cancelled
        ],
        deleted,
        name=_('Delete'),
        description=_("Delete the initiative if you don't want it to appear in your reporting. "
                      "The initiative will still be available in the back office."),
        automatic=False,
        effects=[
            DeleteActivities,
        ]
    )

    restore = Transition(
        [
            rejected,
            cancelled,
            deleted
        ],
        draft,
        name=_('Restore'),
        description=_("The status of the initiative is set to 'Draft'. "
                      "The initiator can edit and submit the initiative again."),
        automatic=False,
        permission=is_staff,
    )
