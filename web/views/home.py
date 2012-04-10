from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.template import RequestContext, loader
import json
from web.models import Category, Submission, VoteCategory

def index(request):
    t = loader.get_template('home/index.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}],
        'parent_categories': Category.objects.filter(parent=None),
        'vote_categories': VoteCategory.objects.all(),
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
        if c.video: c.video = [v for v in json.loads(c.video)]

    if request.user.is_authenticated():
        for c in content:
            ratings = c.votes.filter(user=request.user)
            c.user_rating = {}
            if ratings.count() > 0:
                for r in ratings:
                    c.user_rating[int(r.v_category.id)] = int(r.rating)

    t = loader.get_template('home/index.html')
    c = RequestContext(request, {
        'breadcrumbs': breadcrumbs,
        'content': content,
        'parent_category': parent,
        'parent_categories': Category.objects.filter(parent=None),
        'selected_category': category,
        'vote_categories': VoteCategory.objects.all(),
    })
    return HttpResponse(t.render(c))

def post(request, sid):
    s = Submission.objects.get(id=sid)
    s.video = [v for v in json.loads(s.video)]
    breadcrumbs = [{'url': reverse('home'), 'title': 'Home'}]

    parent_categories = s.tags.filter(parent=None)
    if len(parent_categories) >= 1:
        parent = parent_categories[0]
        breadcrumbs.append({'url': reverse('category', args=[parent.id]), 'title': parent})
    else: parent = None

    categories = s.tags.filter( ~Q(parent=None) )
    if len(categories) >= 1: 
        category = categories[0]
    else: category = None

    if parent == None:
        c = category.parent.all()
        if len(c) > 0:
            c = category.parent.all()[0]
            breadcrumbs.append({'url': reverse('category', args=[c.id]), 'title': c})
                
    if category:
        breadcrumbs.append({'url': reverse('category', args=[category.id]), 'title': category})

    t = loader.get_template('home/index.html')
    c = RequestContext(request, {
        'breadcrumbs': breadcrumbs,
        'content': [s],
        'parent_category': parent,
        'parent_categories': Category.objects.filter(parent=None),
        'selected_category': category,
    })
    return HttpResponse(t.render(c))
