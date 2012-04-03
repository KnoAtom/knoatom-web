from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from web.models import Category, Submission
import re

def validate_youtube_video_id(value):
    regex_vid_id = re.compile('[A-Za-z0-9-_]{11}')
    if not regex_vid_id.match(value):
        raise ValidationError(u'%s is not a valid YouTube video id.' % value)

class SubmissionForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)
    video = forms.CharField(max_length=100, validators=[validate_youtube_video_id], help_text='Please enter an 11 character YouTube video id (multiple allowed, separated by spaces). e.g. http://www.youtube.com/watch?v=VIDEO_ID')
    tags = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.SelectMultiple(attrs={'size':'8'}), help_text='Please select relevant tags for your submission.')
