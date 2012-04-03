from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    prereq = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="postreq")
    parent = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="child")

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Submission(models.Model):
    owner = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    video = models.CharField(max_length=400)
    date_created = models.DateTimeField(auto_now_add=True, default=datetime.now)
    date_modified = models.DateTimeField(auto_now=True, default=datetime.now)
    tags = models.ManyToManyField(Category)

    def __unicode__(self):
        return self.title

class Vote(models.Model):
    user = models.ForeignKey(User)
    submission = models.ForeignKey(Submission, related_name='votes')
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.rating
