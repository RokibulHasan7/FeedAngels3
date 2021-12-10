from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages

from .forms import SignUpForm
from .models import CustomUser, Volunteer

def home(request):
    return render(request, 'auth/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})


def pickup(request):
    return render(request, 'auth/pickup.html')


def volunteerSignUp(request, userid):
    user = CustomUser.objects.get(id=userid)

    if request.method == 'GET':
        return render(request, 'auth/volunteer_signup.html', {'data': user})

    elif request.method == 'POST':
        try:
            volunteer = Volunteer()
            volunteer.username = user
            volunteer.address = request.POST.get('address')
            if len(request.FILES) != 0:
                volunteer.img = request.FILES['img']

            volunteer.save()
            messages.success(request, "Registered Successfully")
        except Exception as e:
            messages.success(request, "Failed to Register Try Again")
            return redirect('/')
    return render(request, 'auth/volunteer_signup.html')


def VolunteerProfile(request, volunteerId):
    getVolunteer = Volunteer.objects.get(username=volunteerId)
    volunteer = Volunteer.objects.all()
    context = {'volunteer': volunteer, 'data': getVolunteer}
    if request.method == 'GET':
        return render(request, 'auth/volunteerProfile.html', context)
    return render(request, 'auth/volunteerProfile.html')