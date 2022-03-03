from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages

from main import settings
from .models import *
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.files.storage import FileSystemStorage
import datetime

from django.core import mail
from django.core.mail import EmailMessage, EmailMultiAlternatives

from django import template

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, smart_bytes, smart_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.html import strip_tags
from django.template.loader import render_to_string 
from .tokens import account_activation_token


# Create your views here.

def test(request):
    template_name = 'base_auth.html'
    
    context = {

    }
    return render(request, template_name, context)



def user_login(request):

    # we request the user
    a_user = request.user

    if a_user.is_authenticated:
        message = "Login"

        return render(request, 'account/auth_already.html', {'user': a_user, 'message': message})
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(request,
                                    username=cd['username'],
                                    password=cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        
                        return redirect('login')
                        # return redirect('dashboard')
                    else:
                        return HttpResponse('Disabled account')
                else:
                    messages.warning(request, "Please enter a correct username and password. Note that both fields may be case-sensitive.")
                    return redirect('login')
        else:
            form = LoginForm()
            return render(request, 'account/login.html', {'form': form})



# to resend the account activation email 
def resend_activate(user_email):

    try:
        new_user = User.objects.get(email=user_email)

        # current_site = get_current_site(request)

        subject = 'Activate Your Account.'
        html_message = render_to_string('account/acc_active_emailBad.html',
                                        {
                                            'user': new_user,
                                            # 'domain': current_site.domain,
                                            'domain': 'the-testing.com',
                                            'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                                            'token': account_activation_token.make_token(new_user),
                                        })
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = user_email

        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    except User.DoesNotExist:
        return HttpResponse()



def register(request):
        
    # we request the user
    a_user = request.user

    if a_user.is_authenticated:
        message = "Register"

        return render(request, 'account/auth_already.html', {'user': a_user, 'message': message})
    else:

        if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                # Create a new user object but avoid saving it yet
                new_user = user_form.save(commit=False)

                cd = user_form.cleaned_data

                try:
                    user_exist = User.objects.get(email=cd['email'])
                    if user_exist:
                        messages.warning(request, "User with this email already exists.")
                        return redirect('register')
                except User.DoesNotExist:
                    pass
                
                if cd['password'] != cd['password2']:

                    messages.warning(request, "Unsuccesful registration. Please make sure your passwords match.")
                    
                    return redirect('register')
                else:
                    
                    # Set the chosen password
                    new_user.set_password(
                        user_form.cleaned_data['password'])
                        
                    # we deactivate the account until email confirmation
                    new_user.is_active = False

                    # Save the User object
                    new_user.save()

                    try:
                        current_site = get_current_site(request)

                        subject = 'Activez votre compte Ethikdo.'

                        relativeLink = reverse(
                            "activate", kwargs={
                                'uidb64': urlsafe_base64_encode(smart_bytes(new_user.id)),
                                "token": account_activation_token.make_token(new_user)
                                }
                            )   
                            
                        absurl = current_site.domain + relativeLink

                        htmltemp = template.loader.get_template('account/account_active_email.html')
                        plaintext = template.loader.get_template('account/account_active_email.txt')

                        message = {
                            'domain': current_site.domain,
                            'absurl': absurl,
                            'user': new_user,
                            'uidb64': urlsafe_base64_encode(smart_bytes(new_user.id)),
                            "token": account_activation_token.make_token(new_user)
                        }

                        text_content = plaintext.render(message)
                        html_content = htmltemp.render(message)

                        msg = EmailMultiAlternatives(subject, text_content, 'Ethikdo <d.ellbouss@gmail.com>', [new_user.email], headers = {'Reply-To': 'no-reply@ethikdo.fr'})
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()

                    except Exception as e:
                        print("\n")
                        print("************************* Exception caught in Register send mail ***************************")
                        print(e)
                        pass
                    
                    return render(request, 'account/register_done.html', {'new_user': new_user})
            else:

                user_form = request.POST

                # Check to see if any users already exist with this email as a username.
                try:
                    match = User.objects.get(email=user_form.get('email'))
                    if match:
                        # A user was found with this as a username, raise an error.
                        # raise forms.ValidationError('This email address is already used.')
                        messages.warning(request, "This email address is already used.")

                        return redirect('register')
                except User.DoesNotExist:
                    # Unable to find a user
                    pass

                if user_form.get('password') != user_form.get('password2'):

                    messages.warning(request, "Unsuccessful registration. Please make sure your passwords match.")

                    return redirect('register')

                messages.warning(request, "Ooops. Something went wrong ... Try again. ")
                return redirect('register')
        else:
            user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form,})


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        messages.success(request, "Your Account has been successfully activated ! ")
        return redirect('dashboard')
    else:
        return HttpResponse('Activation link is invalid! Contact your Admin.')


@login_required(redirect_field_name='login')
@require_GET
def profile(request):
    user = request.user
    
    if user.account_type == '1':
        template_name = 'account/profile_normal.html'
    else :
        template_name = 'account/profile.html'
    
    user_form = UserEditForm(instance=request.user)
    pform = PasswordChangeForm(request.user)
    
    context = {
        'user': user,
        'user_form': user_form, 
        'pform': pform
        }
    
    return render(request, template_name, context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES)
        
        if user_form.is_valid(): 
            
            # we request the user
            user = request.user

            profile_form = user_form.save(commit=False)

            user.username = profile_form.username
            user.first_name = profile_form.first_name
            user.last_name = profile_form.last_name
            user.email = profile_form.email

            if request.POST.get('date_of_birth'):
                user.date_of_birth = request.POST.get('date_of_birth')

            if request.FILES.get('photo'):
                user.photo = request.FILES.get('photo')

            profile_form.save()
            user.save()

            messages.success(request, 'Profile updated successfully')
        else:
            messages.warning(request, 'Error updating your profile')
            
        return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        
    return redirect('profile')


@login_required(redirect_field_name='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.warning(request, 'Please correct the error below in chage password.')
            
    return redirect(reverse('profile') + '#navtabs-profile')

