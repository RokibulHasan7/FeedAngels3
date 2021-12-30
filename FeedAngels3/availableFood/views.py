from django.shortcuts import render
from donation.models import donateFood

def availableFood(request):
    ob = donateFood.objects.all()
    if request.method == 'GET':
        return render(request, 'auth/AvailableFood/availFood.html', {'food': ob})
    return render(request, 'auth/AvailableFood/availFood.html')