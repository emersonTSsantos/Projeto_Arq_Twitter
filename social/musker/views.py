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
        user_profile = UserProfile.objects.get(user=request.user)

        # lógica para seguir ou deixar de seguir
        if request.method == "POST":
            action = request.POST.get('follow')
            if action == "follow":
                user_profile.follows.add(profile)
            elif action == "unfollow":
                user_profile.follows.remove(profile)
            user_profile.save()
            return redirect('profile', pk=pk)

        return render(request, 'profile.html', {
            "profile": profile,
            "user_profile": user_profile
        })
    else:
        messages.success(request, "Você precisa estar logado para visualizar esta página.")
        return redirect('home')
