from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages

from main import settings
from .models import *
# from .forms import *
from account.models import *

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


# Create your views here.


# @login_required()
def dashboard(request):
    
    #
    user = request.user
    
    cards = GiftCard.objects.all()
    cards_number = len(cards)
    
    merchants = User.objects.all().filter(account_type='1')
    merchants_number = len(merchants)
    
    context = {
        'user': user,
        'merchants': merchants,
        'merchants_number': merchants_number,
        'cards': cards,
        'cards_number': cards_number,
        }
        
    return render(request, 'dashboard/dashboard.html', context)


