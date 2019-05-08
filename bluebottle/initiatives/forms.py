from django import forms
from django.utils.translation import ugettext_lazy as _


class InitiativeSubmitForm(forms.Form):
    title = forms.CharField(required=True, label=_('Title'))
    pitch = forms.CharField(required=True, label=_('Pitch'))
    story = forms.CharField(required=True, label=_('Story'))

    class Meta:
        fields = ['title', 'pitch', 'story', 'theme', 'image', 'owner', 'place']
