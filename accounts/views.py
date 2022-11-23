from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode

from accounts.utils import (get_user_dashboard, send_password_reset_email,
                            send_verification_email, user_is_customer,
                            user_is_vendor)
from vendors.forms import VendorForm

from .forms import UserForm
from .models import User, UserProfile


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('dashboard')
    elif request.method == 'POST':
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

            send_verification_email(request, user)

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
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('myAccount')
    elif request.method == 'POST':
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
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = UserProfile.objects.get(user=user)
            vendor.save()

            send_verification_email(request, user)

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


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Congratulations, your account is now ativated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('login')


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login successful")
            return redirect('myAccount')
        else:
            messages.error(request, "Invalid credentials")
            redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request, 'You have been loged out')
    return redirect('login')


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirecturl = get_user_dashboard(user)
    return redirect(redirecturl)


@login_required(login_url='login')
@user_passes_test(user_is_customer)
def customerdashboard(request):
    return render(request, 'accounts/dashboard.html')


@login_required(login_url='login')
@user_passes_test(user_is_vendor)
def vendordashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            send_password_reset_email(request, user)

        messages.success(
            request, 'An email with instructions to reset your password were sent to the email you entered if there was a matching account.')

    return render(request, 'accounts/forgotpassword.html')


def resetpasswordvalidation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('resetpassword')
    else:
        messages.error(
            request, 'Invalid or expired token, unable to reset password.')
        return redirect('login')


def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if password == confirmpassword:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Your password has been reset.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('resetpassword')

    return render(request, 'accounts/resetpassword.html')
