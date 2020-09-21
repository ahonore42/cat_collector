from django.shortcuts import render
from .models import Cat
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect

# Create your views (these are like your controller actions) here.
# CREATE VIEW
# djange will make a create cat form
class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    success_url = '/cats/'

# UPDATE VIEW
class CatUpdate(UpdateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']
    # django hook to grab the primary key (id) of a specific instance of the Cat model
    # form valid will run automatically when this view is hit
    def form_valid(self, form):
        # don't immediately post to the db until we say so
        self.object = form.save(commit=False)
        # access the instance's primary key (id) with self.object.save()
        self.object.save()
        # redirect to the specific model instance's display page by adding the pk (id) to the url
        return HttpResponseRedirect('/cats/' + str(self.object.pk))

# DELETE VIEW
class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats'
        
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def cats_index(request):
    # Get all cats from the db
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats})

def cats_show(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(request, 'cats/show.html', {'cat': cat})