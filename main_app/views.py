from django.shortcuts import render
from .models import Cat
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views (these are like your controller actions) here.

############# USER VIEWS #####################

# USER LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        # try to log the user in
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # django cleaned username and password data required to pass into options
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            # call authenticate and pass in cleaned data as the options
            # authenticate requires ordered options as parameters
            user = authenticate(username = u, password = p)
            # check for valid user data
            
            if user:
                # if the user's account is not disabled
                if user.is_active:
                    # login starts a session for the user in django
                    login(request, user)
                    # redirect to the user's profile page
                    return HttpResponseRedirect('/user/' + u)
                else:
                    print('The account has been disabled')
                    # Todo - handle signup redirect
        else:
            print('The username or password is incorrect')
            # todo handle login redirect
            return HttpResponseRedirect('/login/')
    else:
        # Call in the empty login form, since this will likely be a GET request
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

# USER LOGOUT VIEW
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/cats')

# USER SIGNUP VIEW
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/user' + str(user))
        else:
            return HttpResponse('<h1>Try Again</h1>')
    else:
        # new user form with empty data for GET method
        form = UserCreationForm()
        # render the signup html page
        return render(request, 'signup.html', {'form': form})

# USER PROFILE VIEW
@login_required
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
@method_decorator(login_required, name='dispatch')
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
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

def cats_index(request):
    # Get all cats from the db
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats})

def cats_show(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(request, 'cats/show.html', {'cat': cat})