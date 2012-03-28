from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import Context, loader
from web.models import Category
from web.forms.account import LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.post)
        if(form.is_valid()):
            # log in user
            return HttpResponseRedirect(reverse('home'))
    else:
        form = LoginForm()

    t = loader.get_template('account/login.html')
    c = Context({
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}, {'url':reverse('login'), 'title': 'Login'}],
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))
