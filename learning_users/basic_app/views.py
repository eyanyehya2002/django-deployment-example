from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfo, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

@login_required
def func(request):
    return HttpResponse("I just added this")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False

    #when submit is clicked
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            #saving user_form to data base MUST SAVE TO USE THE .SET_PASSWORD FUNCTION!! THIS IS DIFFERENT TO NORMAL SAVE as its using the authentication and auth... User
            x = user_form.save()
            #hashing password and saving
            x.set_password(x.password)
            x.save()

            #saving portfolio_site and portfolio_pic
            profile = profile_form.save(commit=False)
            profile.user = x

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html', {'user_form':user_form, 'profile_form':profile_form, 'registered': registered})

#Don't call function anything imported
def user_login(request):

    if request.method == 'POST':
        #'username' and 'password' are the for and name in login.html
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        #if user is authenticated
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Someone tried to login and failed!")
            print(f"Username: {username} and password {password}")
            return HttpResponse("Invalid login details supplied")

    else:
        return render(request, 'basic_app/login.html', {})
