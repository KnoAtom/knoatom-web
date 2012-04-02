from django import forms
from django.core.exceptions import ValidationError
import re

def validate_youtube_video_id(value):
    regex_vid_id = re.compile('[A-Za-z0-9-_]{11}')
    if not regex_vid_id.match(value):
        raise ValidationError(u'%s is not a valid YouTube video id.' % value)

class SubmissionForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)
    video = forms.CharField(max_length=100, validators=[validate_youtube_video_id], help_text='Please enter a 11 character YouTube video id.')
