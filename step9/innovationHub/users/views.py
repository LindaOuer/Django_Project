from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    if request.user.is_authenticated:
        # To block the user from accessing register.html when he is already identified
        return redirect('home')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()  # Automatically saves the user and encryptes the password
                username = form.cleaned_data.get('username')
                # flash messages - designated space can be found in base.html
                messages.success(request, f'Account created - {username}')
                return redirect('home')
        else:  # No information has been sent, we create an empty form
            form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')
