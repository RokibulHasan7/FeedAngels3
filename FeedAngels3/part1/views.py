from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .forms import SignUpForm, VolunteerForm
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
    return render(request, 'auth/signup.html', { 'form' : form })


def volunteer_signup(request, userid):
    getuser = CustomUser.objects.get(id=userid)
    if request.method == "GET":
        return render(request, 'auth/volunteer_signup.html', {'data': getuser})
    elif request.method == "POST":
        prod = Volunteer()
        prod.username = getuser
        prod.address = request.POST.get('address')

        if len(request.FILES) != 0:
            prod.image = request.FILES['image']

        prod.save()
        messages.success(request, "Volunteer Added Successfully")
        return redirect('/')
    return render(request, 'auth/volunteer_signup.html')

def VolunteerProfile(request):
    volunteer = Volunteer.objects.all()
    context = {'volunteer':volunteer}
    return render(request, 'auth/VolunteerProfile.html', context)