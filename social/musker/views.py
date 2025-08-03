from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Meep, UserProfile
from .forms import MeepForm

def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        if request.method == "POST": 
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                messages.success(request, "Publicação criada com sucesso!")
                return redirect('home')

        meeps = Meep.objects.all().order_by('-created_at')
        return render(request, 'home.html', {"meeps": meeps, "form": form})
    else:
        meeps = Meep.objects.all().order_by('-created_at')
        return render(request, 'home.html', {"meeps":meeps})

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
        meeps = Meep.objects.filter(user_id=pk)

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
            "user_profile": user_profile,
            "meeps": meeps
        })
    else:
        messages.success(request, "Você precisa estar logado para visualizar esta página.")
        return redirect('home')
