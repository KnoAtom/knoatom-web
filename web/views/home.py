from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.template import Context, loader
from web.models import Category, Submission

def index(request):
    t = loader.get_template('home/index.html')
    c = Context({
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}],
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))

def category(request, cat):
    category = Category.objects.filter(id=cat)[0]
    parents = category.parent.all()
    breadcrumbs = [{'url': reverse('home'), 'title': 'Home'}]

    if len(parents) == 0:
        parent = category
    else:
        parent = parents[0]
        breadcrumbs.append({'url': reverse('category', args=[parent.id]), 'title': parent})

    breadcrumbs.append({'url': reverse('category', args=[category.id]), 'title': category})

    content = None
    if len(parents) == 1: # we are at a specific category
        content = Submission.objects.filter( Q(tags=category) | Q(tags=parent) ).distinct()

    t = loader.get_template('home/index.html')
    c = Context({
        'breadcrumbs': breadcrumbs,
        'selected_category': category,
        'parent_category': parent,
        'category_children': category.child.all(),
        'parent_categories': Category.objects.filter(parent=None),
        'content': content,
    })
    return HttpResponse(t.render(c))
