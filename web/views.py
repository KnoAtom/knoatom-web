from django.template import Context, loader
from django.http import HttpResponse

def index(request):
    t = loader.get_template('home/index.html')
    c = Context({
        'title': 'pine nuts'
    })
    return HttpResponse(t.render(c))
