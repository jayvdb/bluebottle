from django.conf import settings
from django.template.defaultfilters import slugify
from django.db import models
from django.utils.translation import ugettext as _
from django.core.files.storage import FileSystemStorage
from django_extensions.db.fields import (CreationDateTimeField,
                                         ModificationDateTimeField)

from taggit.managers import TaggableManager
from djchoices import DjangoChoices, ChoiceItem


class Organization(models.Model):
    """
    Organizations can run Projects. An organization has one or more members.
    """
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)

    created = CreationDateTimeField(_('created'))
    updated = ModificationDateTimeField(_('updated'))
    deleted = models.DateTimeField(_('deleted'), null=True, blank=True)

    partner_organizations = models.TextField(_('partner organizations'),
                                             blank=True)

    # Address
    address_line1 = models.CharField(max_length=100, blank=True)
    address_line2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.ForeignKey('geo.Country', blank=True, null=True,
                                related_name='country')
    postal_code = models.CharField(max_length=20, blank=True)

    # Contact
    phone_number = models.CharField(_('phone number'), max_length=40,
                                    blank=True)
    website = models.URLField(_('website'), blank=True)

    email = models.EmailField(blank=True)

    tags = TaggableManager(blank=True, verbose_name=_('tags'))

    registration = models.FileField(upload_to='organizations/registrations',
                                    storage=FileSystemStorage(
                                        location=settings.PRIVATE_MEDIA_ROOT),
                                    null=True,
                                    blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.name)
            slug = original_slug
            next_slug = 2
            while not slug or self.__class__.objects.filter(slug=slug):
                slug = '{0}-{1}'.format(original_slug, next_slug)
                next_slug += 1
            self.slug = slug

        super(Organization, self).save(*args, **kwargs)

    def merge(self, organizations):
        """ Merge `organizations` into the current organization.
        Makes sure that all foreign keys point to `this`.

        Deletes all organization models in `organization` after merging.
        """
        for organization in organizations:
            for member in organization.members.all():
                member.organization = self
                member.save()

            for project in organization.projects.all():
                project.organization = self
                project.save()

            organization.delete()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")


class OrganizationContact(models.Model):
    """
    Basic details for an organization contact
    """
    name = models.TextField(_('name'), max_length=100)
    email = models.EmailField(_('email'), max_length=254)
    phone = models.TextField(_('phone'), max_length=40)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('creator'))
    organization = models.ForeignKey('organizations.Organization',
                                     related_name="contacts")
    created = CreationDateTimeField(
        _('created'), help_text=_('When this contact was created.'))
    updated = ModificationDateTimeField(_('updated'))


class OrganizationMember(models.Model):
    class MemberFunctions(DjangoChoices):
        owner = ChoiceItem('owner', label=_('Owner'))
        editor = ChoiceItem('editor', label=_('Editor'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'))
    function = models.CharField(_('function'),
                                max_length=20,
                                choices=MemberFunctions.choices)
    organization = models.ForeignKey('organizations.Organization',
                                     related_name="members")
    created = CreationDateTimeField(_('created'))
    updated = ModificationDateTimeField(_('updated'))
    deleted = models.DateTimeField(_('deleted'), null=True, blank=True)

    class Meta:
        verbose_name = _('organization member')
        verbose_name_plural = _('organization members')
