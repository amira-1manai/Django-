from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        # Redirect already logged-in users to the home page
        return redirect('home')  # Change 'home' to the page you want to redirect to

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}")
                return redirect('home')  # Redirect to home or desired page after login
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect('login')