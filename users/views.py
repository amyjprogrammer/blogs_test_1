from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Register new users"""
    if request.method != 'POST':
        #haven't registered yet. Provide a blank form
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #Log the user in and redirect to home page
            login(request, new_user)
            return redirect ('blogs:blogs')

    #Display a blank or invalid form
    context = {'form': form}
    return render(request, 'registration/register.html', context)
