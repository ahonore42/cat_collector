from django.shortcuts import render
from .models import Cat
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# Create your views (these are like your controller actions) here.

############# USER VIEWS #####################

# USER LOGIN VIEW
def login_view(request):
    if request.method == 'POST'
        # try to log the user in
    else:
        # Call in the login form, since this will likely be a GET request
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

# USER PROFILE VIEW
def profile(request, username):
    user = User.objects.get(username=username)
    # grab the user by username
    cats = Cat.objects.filter(user=user)
    # user field in the cat table needs to match
    # cats returned are specific to the username
    return render(request, 'profile.html', {'username': username, 'cats': cats})
    # render the profile html page with the user's cats

############## CAT VIEWS #####################

# CREATE VIEW
# djange will make a create cat form
class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    success_url = '/cats/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/cats')

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

################ DEFAULT VIEWS ###############
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