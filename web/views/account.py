from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
import random, string
from web.forms.account import *
from web.models import Category

@login_required()
def index(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, error_class=PlainErrorList)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['new_password']:
            user = User.objects.get(pk=request.user.id)
            if user:
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, 'Your password has been changed.')
                return HttpResponseRedirect(reverse('account'))
        messages.warning(request, 'Could not change your password. Make sure you type the same password twice in the form below')
    else:
        form = ChangePasswordForm(error_class=PlainErrorList)

    t = loader.get_template('account/index.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}, {'url':reverse('account'), 'title': 'Account'}],
        'form': form,
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))

def forgot_password(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, error_class=PlainErrorList)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])
            if user:
                new_password = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(10))
                send_mail('Knoatom Password Reset', 'You requested to reset your password at knoatom.eecs.umich.edu. Here is your new password: ' + new_password + '\n\nIf you did not request this change, contact us immediatly.\n\n-- The Management', 'knoatom-webmaster@umich.edu', [user.email])
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
                if user.is_active == 0:
                    messages.warning(request, 'Please activate your account before you log in.')
                    return HttpResponseRedirect(reverse('login'))
                auth_login(request, user)
                if form.cleaned_data['redirect']: return HttpResponseRedirect(form.cleaned_data['redirect'])
                return HttpResponseRedirect(reverse('home'))
        messages.warning(request, 'Could not authenticate you. Try again.')
    else:
        form = LoginForm(initial={'redirect': request.GET.get('next', None),}, error_class=PlainErrorList)

    t = loader.get_template('account/login.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}, {'url':reverse('login'), 'title': 'Login'}],
        'login_form': form,
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))

@login_required()
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))

class PlainErrorList(ErrorList):
    def __unicode__(self):
        return self.as_plain()
    def as_plain(self):
        if not self: return u''
        return u'<br/>'.join([ e for e in self ])

import hashlib

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = RegisterForm(request.POST, error_class=PlainErrorList)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password']);
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            user.is_active = False
            user.save()
            m = hashlib.md5()
            m.update(user.email + str(user.date_joined).split('.')[0])
            send_mail('Knoatom Registration', 'You have successfully registered at knoatom.eecs.umich.edu with the username ' + user.username + '. Please validate your account by going to ' + request.build_absolute_uri('validate') + '?email=' + user.email + '&validation=' + m.hexdigest() + ' . If you did not process this registration, please contact us as soon as possible.\n\n-- The Management', 'knoatom-webmaster@umich.edu', [user.email])
            messages.success(request, 'You have been registered. Please login to continue.')
            return HttpResponseRedirect(reverse('login'))
        messages.warning(request, 'Could not register you. Try again.')
    else:
        form = RegisterForm(error_class=PlainErrorList)

    t = loader.get_template('account/register.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}, {'url':reverse('register'), 'title': 'Register'}],
        'register_form': form,
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))

def validate(request):
    if request.user.is_authenticated():
        messages.warning(request, 'You are already confirmed.')
        return HttpResponseRedirect(reverse('home'))
    if request.GET.get('validation', None) and request.GET.get('email', None):
        user = User.objects.get(email=request.GET.get('email'))
        m = hashlib.md5()
        m.update(user.email + str(user.date_joined))
        if m.hexdigest() == request.GET.get('validation'):
            user.is_active = True
            user.save()
            messages.success(request, 'Thank you for validating your email!')
            return HttpResponseRedirect(reverse('account'))
        else:
            messages.warning(request, 'There was an error processing your validation.')
            return HttpResponseRedirect(reverse('login'))

    messages.warning(request, 'Your reached a page in an invalid manner.')
    return HttpResponseRedirect(reverse('home'))
