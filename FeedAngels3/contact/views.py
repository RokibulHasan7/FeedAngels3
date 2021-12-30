from django.shortcuts import render, redirect
from .models import contact

# Create your views here.
def contact_us(request):
    if request.method == "POST":
        con = contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        con.name = name
        con.email = email
        con.message = message
        con.save()
        return redirect('home')
    return render(request, 'auth/contact_us.html')
