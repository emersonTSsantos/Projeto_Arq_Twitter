from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Meep, UserProfile
from .forms import MeepForm, ProfilePicForm, SignUpForm, UpdateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

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
    

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso.")
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "Você foi desconectado")
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso.")
            return redirect('home')
        
    return render(request, 'register.html', {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = UserProfile.objects.get(user_id=request.user.id)
        
        #Get forms
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)  # Re-login to update session
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect('home')
        
        return render(request, 'update_user.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        messages.success(request, "Você precisa estar logado para atualizar seu perfil.")
        return redirect('home')
    
@login_required
def update_user(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = ProfilePicForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('profile', request.user.id)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = ProfilePicForm(instance=request.user.userprofile)
    return render(request, 'update_user.html', {'user_form': user_form, 'profile_form': profile_form})

def meep_like(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if request.user in meep.likes.all():
        meep.likes.remove(request.user)
    else:
        meep.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

def meep_share(request, pk):
    original_meep = get_object_or_404(Meep, id=pk)
    if request.user.is_authenticated:
        Meep.objects.create(
            user=request.user,
            body=original_meep.body,
            shared_from=original_meep
        )
        messages.success(request, "Publicação compartilhada com sucesso.")
    return redirect('home')