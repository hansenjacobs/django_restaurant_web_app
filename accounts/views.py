from multiprocessing import context
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from vendors.models import Vendor

from .forms import UserForm
from .models import User, UserProfile
from vendors.forms import VendorForm

# Create your views here.


def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Create User directly w/ Object
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()
            # return redirect('registerUser')

            # Create User using Object Method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone_number']

            user = User.objects.create_user(
                first_name, last_name, username, email, password)
            user.phone_number = phone
            user.role = User.CUSTOMER
            user.save()

            messages.success(request, 'Your account has been created.')

            return redirect('registerUser')
        else:
            pass
    else:
        form = UserForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context=context)


def registerVendor(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone_number']
            user = User.objects.create_user(
                first_name, last_name, username, email, password)
            user.phone_number = phone
            user.role = User.RESTAURANT
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = UserProfile.objects.get(user=user)
            vendor.save()
            messages.success(request,
                             'Your account has been requested. Please wait for approval.')
            return redirect('registerVendor')
        else:
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

        context = {
            'form': form,
            'v_form': v_form,
        }

    return render(request, 'accounts/registerVendor.html', context=context)


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return


def dashboard(request):
    return
