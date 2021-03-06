from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.views import generic
from django.views.generic import ListView
from django.db.models import Q

from .forms import SignUpForm
from .models import CustomUser, Volunteer, PickUppoints
from donation.models import donateMoney, donateFood


from django.contrib.auth import get_user_model

from blog.forms import PostForm

User = get_user_model()


def home(request):
    volunteer = Volunteer.objects.all()
    context = {'data': volunteer}
    # if request.method == 'GET':
    # return render(request, 'auth/volunteerProfile.html', context)
    return render(request, 'auth/home.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})


def pickup(request):
    return render(request, 'auth/pickup.html')


class pickupPointSearchResult(generic.ListView):
    model = PickUppoints
    template_name = 'auth/pickupPointSearchResult.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = PickUppoints.objects.filter(Q(District__icontains=query))
        return object_list


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
            return redirect('home')
        except Exception as e:
            messages.success(request, "Failed to Register Try Again")
            return redirect('/')
    return render(request, 'auth/volunteer_signup.html')


def VolunteerProfile(request, volunteerId):
    getVolunteer = Volunteer.objects.get(username=volunteerId)
    context = {'data': getVolunteer}
    if request.method == 'GET':
        return render(request, 'auth/volunteerProfile.html', context)
    return render(request, 'auth/volunteerProfile.html')


def UserProfile(request, userid):
    getUser = CustomUser.objects.get(id=userid)
    donateHistory1 = donateMoney.objects.all()
    donateHistory2 = donateFood.objects.all()
    context = {'getUser': getUser, 'donateHistory1': donateHistory1, 'donateHistory2': donateHistory2}
    if request.method == 'GET':
        return render(request, 'auth/UserProfile.html', context)
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
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Feed Angels',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="auth/password/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def editProfile(request):
    if request.POST:
        user = User.objects.get(pk=request.user.id)
        user.full_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.mobileNum = request.POST.get('mobileNum')
        user.save()
    return render(request, 'auth/editProfile.html')


def aboutUs(request):
    return render(request, 'auth/aboutUs.html')


