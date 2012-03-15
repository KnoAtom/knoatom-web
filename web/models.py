from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

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
    date_created = models.DateTimeField(auto_now_add=True, default=datetime.now)
    date_modified = models.DateTimeField(auto_now=True, default=datetime.now)
    tags = models.ManyToManyField(Category)

    def __unicode__(self):
        return self.title
