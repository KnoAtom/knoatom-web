from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.template import RequestContext, loader
import json
from web.models import Category, Submission

def index(request):
    t = loader.get_template('home/index.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}],
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))

def category(request, cat):
    category = Category.objects.get(id=cat)
    parents = category.parent.all()
    breadcrumbs = [{'url': reverse('home'), 'title': 'Home'}]

    if len(parents) == 0:
        parent = category
        content = Submission.objects.filter( Q(tags=category) | Q(tags__in=category.child.distinct()) ).distinct()
    else:
        parent = parents[0]
        content = Submission.objects.filter( Q(tags=category) ).distinct()
        breadcrumbs.append({'url': reverse('category', args=[parent.id]), 'title': parent})

    breadcrumbs.append({'url': reverse('category', args=[category.id]), 'title': category})

    # un-json-fy the videos
    for c in content:
        c.video = [v for v in json.loads(c.video)]

    if request.user.is_authenticated():
        for c in content:
            ratings = c.votes.filter(user=request.user)
            if ratings.count() == 1:
                c.user_rating = ratings[0].rating

    t = loader.get_template('home/index.html')
    c = RequestContext(request, {
        'breadcrumbs': breadcrumbs,
        'selected_category': category,
        'parent_category': parent,
        'category_children': category.child.all(),
        'parent_categories': Category.objects.filter(parent=None),
        'content': content,
    })
    return HttpResponse(t.render(c))
