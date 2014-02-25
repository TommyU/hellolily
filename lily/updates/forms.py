from django import forms
from django.utils.translation import ugettext as _

from lily.updates.models import BlogEntry


class CreateBlogEntryForm(forms.ModelForm):

    class Meta:
        model = BlogEntry
        fields = ('reply_to', 'content',)
        exclude = ('author', 'created', 'deleted',)
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': _('Write something here'),
                'click_show': False,
                'field_classes': 'blogentry-textarea inline',
                'maxlength': 255,
            }),
            'reply_to': forms.HiddenInput(),
        }