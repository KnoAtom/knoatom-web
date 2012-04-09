from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
import random, string, re
from web.forms.admin import *
from web.models import Category, User

@login_required()
def batch_add(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        form = BatchAddUsersForm(request.POST, error_class=PlainErrorList)
        if form.is_valid():
            users_added = 0
            for u in form.cleaned_data['users'].split('\n'):
                u = u.strip()
                if u == '': continue
                user_search = User.objects.filter( Q(email=u) | Q(username=u) )
                if not re.match('[a-z]*@umich\.edu', u) or len(user_search) > 0:
                    messages.warning(request, 'Could not add ' + u + '. Username or email are already in the database, or email is not uniqname@umich.edu.')
                    continue
                password = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(10))
                user = User.objects.create_user(email=u, username=u)
                user.set_password(password)
                user.save()
                users_added += 1
                send_mail('KnoAtom New Account', 'You have been registered at knoatom.eecs.umich.edu. Your information is as follows:\n\nUsername: ' + u + '\nPassword: ' + password + '\n\nPlease login and change your password as soon as you can (click on your username at the bottom of the left sidebar).\n\nThank you\n\n-- The Management', 'knoatom-webmaster@umich.edu', [u, 'knoatom-webmaster@umich.edu'])
            messages.success(request, str(users_added) + ' users have been added.')
        else:
            messages.warning(request, 'Could not add users. Did you have the format correct?')
    else:
        form = BatchAddUsersForm(error_class=PlainErrorList)

    t = loader.get_template('admin/batch_add.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}, {'url':reverse('batch_add'), 'title': 'Batch Add'}],
        'form': form,
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))
