from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .forms import SignUpForm
from .models import CustomUser, Volunteer

from django.contrib.auth import get_user_model
User = get_user_model()

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



def UserProfile(request, userid):
    getUser = CustomUser.objects.get(id=userid)
    if request.method == 'GET':
        return render(request, 'auth/UserProfile.html', {'data': getUser})
    return render(request, 'auth/UserProfile.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'auth/changePassword.html', {
        'form': form
    })


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "auth/password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Feed Angels',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="auth/password/password_reset.html", context={"password_reset_form":password_reset_form})