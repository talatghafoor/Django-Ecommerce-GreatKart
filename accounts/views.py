from django.shortcuts import render, redirect
from .forms import RegisterationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

#Verifi
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_no = form.cleaned_data['phone_no']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_no = phone_no
            user.save()
            # User Activation 
            # current_site = get_current_site(request)
            # mail_subject = 'Please Activate Your Account'
            # message = render_to_string('accounts/account_verification_email.html', {
            #     'user' : user,
            #     'domain' : current_site,
            #     'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token' : default_token_generator.make_token(user),

            # })
            # to_email = email
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.send()
            messages.success(request, 'Registration Successfull')
            return redirect('register')
    else:
        form = RegisterationForm
    context = {
    'form': form
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now Logged In.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Login Credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are Logged Out')
    return redirect('login')

def activate(request, uidb64, token):
    return

@login_required(login_url= 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')