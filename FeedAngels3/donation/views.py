from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import donateMoney, donateFood
from .paytm import generate_checksum, verify_checksum
from part1.models import CustomUser
#from .forms import donateFoodForm
from django.contrib.auth import get_user_model

User = get_user_model()


def donateFoodView(request, userid):
    user = CustomUser.objects.get(id=userid)
    if request.method == "GET":
        return render(request, 'auth/donateFood.html', {'data': user})
    elif request.method == "POST":
        try:
            district = request.POST['district']
            address = request.POST['address']
            description = request.POST['description']
            expiration_date = request.POST['expiration_date']
            donate_food = donateFood.objects.create(made_by=user, district=district, address=address,
                                                    description=description,
                                                    expiration_date=expiration_date, is_approved=0)
            donate_food.save()
            return redirect('home')
        except:
            messages.success(request, "Failed to Donate! Try Again...")
            return redirect('/')


def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'auth/donateMoney.html')
    try:
        username = request.POST['username']
        password = request.POST['password']
        amount = int(request.POST['amount'])
        user = authenticate(request, username=username, password=password)
        if user is None:
            raise ValueError
        auth_login(request=request, user=user)
    except:
        return render(request, 'auth/donateMoney.html', context={'error': 'Wrong Account Details or amount'})

    transaction = donateMoney.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'auth/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        paytm_checksum = ''
        print(request.body)
        print(request.POST)
        received_data = dict(request.POST)
        print(received_data)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            print("Checksum Matched")
            received_data['message'] = "Checksum Matched"
        else:
            print("Checksum Mismatched")
            received_data['message'] = "Checksum Mismatched"

        return render(request, 'auth/callback.html', context=received_data)


def donation(request):
    return render(request, 'auth/donation.html')


""""
def donateFood(request, userid):
    user = CustomUser.objects.get(id=userid)
    if request.method == 'GET':
        return render(request, 'auth/donateFood.html', {'data': user})
    elif request.method == 'POST':
        try:
            donate_food = donateFood()
            donate_food.made_by = user
            donate_food.district = request.POST.get('district')
            donate_food.address = request.POST.get('address')
            donate_food.description = request.POST.get('description')
            donate_food.expiration_date = request.POST.get('expiration_date')
            donate_food.is_approved = 0
            donate_food.save()
            messages.success(request, "Donation done!")
            return redirect('home')
        except Exception as e:
            messages.success(request, "Failed to Donate! Try Again...")
            return redirect('/')
    return render(request, 'auth/donateFood.html')



def donateFood(request, userid):
    user = CustomUser.objects.get(id=userid)
    if request.method == "GET":
        return render(request, 'auth/donateFood.html', {'data': user})
    try:
        district = request.POST['district']
        address = request.POST['address']
        description = request.POST['description']
        expiration_date = request.POST['expiration_date']
        donate_food = donateFood.objects.create(made_by=user, district=district, address=address,
                                                description=description,
                                                expiration_date=expiration_date)
        donate_food.save()
        return redirect('home')
    except:
        messages.success(request, "Failed to Donate! Try Again...")
        return redirect('/')
"""
