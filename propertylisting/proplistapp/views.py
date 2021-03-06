from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.contrib.auth.models import User
from .models import PostAd, UserProfile
from .forms import PostAdForm, UserForm, UserProfileForm

# Create your views here.
def index(request):
    if request.method == "POST":
        form =PostAdForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('propertyAds') 
    else:    
        form = PostAdForm()
        if request.user.is_authenticated:
                return render(request,"PropertyAdForm.html",{'AdData': form})
        else:
            return redirect('loginUser')
        

def propertyAds(request):
    if request.method == 'GET': 
        Houses = PostAd.objects.all()
        return render(request, 'PropertyAds.html', {'houses' : Houses})


def contactUs(request):
    return render(request, 'contactus.html')


def registerUser(request):
    # if this is a POST request we need to process the form data
    template = 'register.html'
   
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password = form.cleaned_data["password"],
                email = form.cleaned_data["email"],
                first_name = form.cleaned_data["first_name"],
                last_name = form.cleaned_data["last_name"],
            )
                # profile_picture = form.cleaned_data['profile_picture'],
                # phone_number = form.cleaned_data['phone_number']
                # form.save()
                # username = form.cleaned_data.get('username')
                # password = form.cleaned_data.get('password')
                # user = authenticate(username=username, password=password)
                #authenticate user then login
                # if user:
                # Login the user
                login(request, user)
                # redirect to home page:
                return redirect('index')
                # else:
                #     return redirect('loginUser')
    # No post data availabe, let's just show the page.
    else:
        form = UserForm()

    return render(request, template, {'form': form})

def loginUser(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return redirect('index')    
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'login.html')    

def logoutUser(request):
    logout(request)
    return redirect('loginUser')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })    