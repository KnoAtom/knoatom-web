from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
import json
from web.forms.submission import SubmissionForm
from web.models import Category, Submission

class PlainErrorList(ErrorList):
    def __unicode__(self):
        return self.as_plain()
    def as_plain(self):
        if not self: return u''
        return u'<br/>'.join([ e for e in self ])

@login_required()
def index(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, error_class=PlainErrorList)
        if form.is_valid():
            s = Submission(owner=request.user)
            s.title = form.cleaned_data['title']
            s.content = form.cleaned_data['content']
            s.video = json.dumps(form.cleaned_data['video'].split(' '))
            s.save()
            s.tags = form.cleaned_data['tags']
            s.save()
            return HttpResponseRedirect(reverse('home'))
        messages.warning(request, 'Error submitting.')
    else:
        form = SubmissionForm(error_class=PlainErrorList)

    t = loader.get_template('submit.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}],
        'form': form,
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))

