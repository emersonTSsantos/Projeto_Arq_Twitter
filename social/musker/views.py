from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile

def home(request):
    return render(request, 'home.html', {})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = UserProfile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, ("Você precisa estar logado para visualizar esta página."))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user_id=pk)
        return render(request, 'profile.html', {"profile": profile})
    else:
        messages.success(request, ("Você precisa estar logado para visualizar esta página."))
        return redirect('home')