from django.contrib import admin
from web.models import Submission, Category, Vote, VoteCategory

admin.site.register(Category)
admin.site.register(Submission)
admin.site.register(Vote)
admin.site.register(VoteCategory)
