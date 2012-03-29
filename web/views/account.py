from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
import random, string
from web.models import Category
from web.forms.account import *

def forgot_password(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, error_class=PlainErrorList)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])
            if user:
                new_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
                print new_password
                send_mail('Knoatom Password Reset', 'You requested to reset your password at knoatom.eecs.umich.edu. Here is your new password: ' + new_password + '\n\nIf you did not request this change, contact us immediatly.\n\n-- The Management', 'bkend@umich.edu', [user.email])
                user.set_password(new_password)
                user.save()
                messages.success(request, 'If we have your email on file, you should expect a password reset within a couple minutes to appear in your inbox.')
                return HttpResponseRedirect(reverse('login'))
    else:
        form = ForgotPasswordForm(error_class=PlainErrorList)

    t = loader.get_template('account/forgot_password.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}, {'url':reverse('login'), 'title': 'Login'}],
        'login_form': form,
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = LoginForm(request.POST, error_class=PlainErrorList)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('home'))
        messages.warning(request, 'Could not authenticate you. Try again.')
    else:
        form = LoginForm(error_class=PlainErrorList)

    t = loader.get_template('account/login.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}, {'url':reverse('login'), 'title': 'Login'}],
        'login_form': form,
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))

class PlainErrorList(ErrorList):
    def __unicode__(self):
        return self.as_plain()
    def as_plain(self):
        if not self: return u''
        return u'<br/>'.join([ e for e in self ])

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    error = None
    if request.method == 'POST':
        form = RegisterForm(request.POST, error_class=PlainErrorList)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password']);
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            user.save()
            messages.success(request, 'You have been registered. Please login to continue.')
            return HttpResponseRedirect(reverse('login'))
        error = 'Could not register you. Try again.'
    else:
        form = RegisterForm(error_class=PlainErrorList)

    t = loader.get_template('account/register.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}, {'url':reverse('register'), 'title': 'Register'}],
        'error': error,
        'register_form': form,
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))
