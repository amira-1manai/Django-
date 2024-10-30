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

    # Add 'form-control' class to each field
    form.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your username'})
    form.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your password'})
    form.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm your password'})

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/fields')  # Change to the page you want to redirect to

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}")
                return redirect('home')
    else:
        form = AuthenticationForm()

    # Add 'form-control' class to each field
    form.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your username'})
    form.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your password'})

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect('login')