from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages

from main import settings
from .models import *
# from .forms import *
from cartkado.models import *
from account.models import *

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.files.storage import FileSystemStorage

import datetime
from datetime import date, datetime

from django.core import mail
from django.core.mail import EmailMessage, EmailMultiAlternatives

from django import template

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, smart_bytes, smart_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.html import strip_tags
from django.template.loader import render_to_string 


# Create your views here.


# @login_required(redirect_field_name='login')
def dashboard(request):
    
    #
    user = request.user
    
    cards = GiftCard.objects.all()
    # cards_number = len(cards)
    
    merchants = User.objects.all().filter(account_type='1')
    merchants_number = len(merchants)
    
    context = {
        'user': user,
        'merchants': merchants,
        'merchants_number': merchants_number,
        'cards': cards,
        'cards_number': len(cards),
        }
        
    return render(request, 'dashboard/dashboard.html', context)



# 
# @login_required(redirect_field_name='login')
def contact(request):
    
    user_allowed = request.user

    if user_allowed.is_authenticated:
        if user_allowed.user_type == "0":

            return redirect('dashboard')


    return render(request, "dashboard/contact.html")


# 
@csrf_exempt
def check_gift_card_exist(request):
    card_title = request.POST.get("card_title")
    card_code = request.POST.get("card_code")
    
    try:
        card_obj = GiftCard.objects.all().filter(code=card_code).exists()

        if card_obj:
            return HttpResponse(True)
    except GiftCard.DoesNotExist:
        # 
        return HttpResponse(False)



@login_required(redirect_field_name='login')
def debit_card(request):

    user_allowed = request.user

    if user_allowed.is_authenticated:
            
        if request.method == 'POST':
            card_code = request.POST.get("card_code")
            debit_amount = float(request.POST.get("debit_amount"))

            try:
                gift_card = GiftCard.objects.get(code=card_code)
                card_amount = gift_card.amount

                if debit_amount > card_amount:
                    status = "Failed: Fond Insuffisant"
                    
                    messages.error(request, "Failed: Fond Insuffisant")
                else:
                    status = "Succeeded"
                    card_amount = GiftCard.objects.get(code=card_code).amount
                    card_amount = card_amount - debit_amount
                    GiftCard.objects.filter(code=card_code).update(amount=card_amount)
                    
                    messages.success(request, "Transaction Completed")

                debit = Debit(
                    card_id=gift_card,
                    user=user_allowed,
                    debit_amount=debit_amount,
                    status=status
                )
                debit.save()
                
                return redirect(reverse("debit_card"))
            except GiftCard.DoesNotExist:
                
                messages.warning(request, "Failed to Complete Transaction")

                return redirect(reverse("debit_card"))

        
        context = {
            "gift_card": GiftCard.objects.all(),
            "user": user_allowed,
        }
        
        return render(request, "dashboard/debit_card.html", context)



@login_required(redirect_field_name='login')
def transaction(request):

    user_allowed = request.user

    if user_allowed.is_authenticated:
        if user_allowed.account_type == "0" or user_allowed.is_superuser:

            # transaction

            debit = Debit.objects.all()
            
            context = {
                "debit": debit,
                "user": user_allowed,
            }

            return render(request, "dashboard/transaction.html", context)

        elif user_allowed.account_type == "1":

            debit = Debit.objects.all().filter(user=user_allowed)
            
            context = {
                "user": user_allowed,
                "debit": debit,
            }

            return render(request, "dashboard/transaction.html", context)


    return redirect("dashboard")
        


@login_required(redirect_field_name='login')
def add_card(request):
    user_allowed = request.user

    if user_allowed.is_authenticated:

        if user_allowed.account_type == "O" or user_allowed.is_superuser:

            if request.method == 'POST':

                card_amount = float(request.POST.get("card_amount"))

                try:
                    card_count = GiftCard.objects.all().count()

                    x = date.today()
                    x = (str(x)).replace("-", "")

                    if card_count == 9:
                        card_code = "CK" + x + "00" + str(card_count+1)
                    elif (card_count / 10) < 1:
                        card_code = "CK" + x + "000" + str(card_count+1)
                    elif ((card_count + 1) / 10) < 10:
                        card_code = "CK" + x + "00" + str(card_count+1)
                    else:
                        card_code = "CK" + x + "0" + str(card_count+1)

                    card_model = GiftCard(amount=card_amount, code=card_code)
                    card_model.save()
                    messages.success(request, "Successfully Added Gift Card")

                    return redirect(reverse("add_card"))
                except Exception as e:
                    print("\n")
                    print("*************** Exception gotten in add card ***************")
                    print(e)
                    messages.error(request, "Failed To Add Gift Card")

                    return redirect(reverse("add_card"))

            return render(request, "dashboard/add_card.html")

    return redirect('dashboard')



# 
@login_required()
def manage_card(request):
    user = request.user

    if user.is_authenticated:
        if user.account_type == "0" or user.is_superuser:

            gift_card = GiftCard.objects.all()
            gift_card_count = gift_card.count()

            return render(request, "dashboard/cards.html",
                          {
                              "gift_card": gift_card,
                              "gift_card_count": gift_card_count,
                          }
                          )

        elif user.account_type == "1":
            
            return redirect('dashboard')

    return redirect('dashboard')



#
@login_required(redirect_field_name='login')
def top_up_card(request):

    user_allowed = request.user

    if user_allowed.is_authenticated:
        
        if user_allowed.account_type == "0" or user_allowed.is_superuser:

            if request.method == 'POST':
                card_id = request.POST.get("card")
                top_amount = request.POST.get("top_amount")
                top_amount = float(top_amount)

                try:
                    gift_card = GiftCard.objects.get(id=card_id)
                    card_amount = gift_card.amount

                    card_amount = card_amount + top_amount

                    GiftCard.objects.filter(id=card_id).update(amount=card_amount)

                    messages.success(request, "Transaction Completed")

                    return redirect(reverse("top_up_card"))
                except GiftCard.DoesNotExist:
                    
                    messages.error(request, "Failed to Complete Transaction.")

                    return redirect(reverse("top_up_card"))

            context = {
                'gift_card': GiftCard.objects.all(),
                'user': user_allowed,
            }
            
            return render(request, "main/admin/top_up_card.html", context)


    return redirect("dashboard")
    
    