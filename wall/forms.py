from django import forms
from .models import Post, Comment
from django.utils.translation import gettext as _

class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = (
            'text',
        )

        labels = {
            'text': _('Go and share something with everybody...'),
        }

        error_messages = {
            'text': {
                'required': _('Please, enter something to share with everybody')
            },
        }
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput) or \
                isinstance(field.widget, forms.Textarea) or \
                isinstance(field.widget, forms.DateInput) or \
                isinstance(field.widget, forms.DateTimeInput) or \
                isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({'placeholder': field.label})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = (
            'text',
        )

        labels = {
            'text': _('Share some thoughts...'),
        }

        error_message = {
            'text': {
                'required': _('Please, enter some thoughts to share')
            }
        },

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput) or \
                isinstance(field.widget, forms.Textarea) or \
                isinstance(field.widget, forms.DateInput) or \
                isinstance(field.widget, forms.DateTimeInput) or \
                isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({'placeholder': field.label})


