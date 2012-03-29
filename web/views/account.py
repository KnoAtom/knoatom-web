from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from web.models import Category
from web.forms.account import LoginForm

class PlainErrorList(ErrorList):
    def __unicode__(self):
        return self.as_plain()
    def as_plain(self):
        if not self: return u''
        return u'<br/>'.join([ e for e in self ])

def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST, error_class=PlainErrorList)
        if form.is_valid():
            user_info = User.objects.filter(email=form.cleaned_data['email'])
            if len(user_info) == 1:
                user_info = user_info[0]
                user = authenticate(username=user_info.username, password=form.cleaned_data['password'])
                if user is not None:
                    auth_login(request, user)
                    return HttpResponseRedirect(reverse('home'))
            error = 'Could not authenticate you. Try again.'
    else:
        form = LoginForm(error_class=PlainErrorList)

    t = loader.get_template('account/login.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}, {'url':reverse('login'), 'title': 'Login'}],
        'error': error,
        'login_form': form,
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))

