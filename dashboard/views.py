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
        # 'cards_number': cards_number,
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
    card_obj = GiftCard.objects.all().filter(code=card_code).exists()

    if card_obj:
        return HttpResponse(True)
    else:
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
                    
                    messages.warning(request, "Failed: Fond Insuffisant")
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
            except Exception as e:
                
                print("\n")
                print("******************** Exception gotten in debit card ********************")
                print(e)
                
                messages.warning(request, "Failed to Complete Transaction")

                return redirect(reverse("debit_card"))

        
        context = {
            "gift_card": GiftCard.objects.all(),
            "user": user_allowed,
        }
        
        return render(request, "dashboard/debit_card.html", context)

    
    #     return redirect('dashboard')

    #     elif user_allowed.account_type == "1":

    #         merchant = User.objects.get(id=user_allowed.id)

    #         if request.method == 'POST':
    #             card_code = request.POST.get("card_code")
    #             debit_amount = float(request.POST.get("debit_amount"))

    #             gift_card = GiftCard.objects.get(code=card_code)
    #             card_amount = gift_card.amount

    #             try:

    #                 if debit_amount > card_amount:
    #                     status = "Failed: Fond Insuffisant"
                        
    #                     messages.warning(request, "Failed: Fond Insuffisant")
    #                 else:
    #                     status = "Succeeded"
    #                     card_amount = GiftCard.objects.get(code=card_code).amount
    #                     card_amount = card_amount - debit_amount
    #                     GiftCard.objects.filter(code=card_code).update(amount=card_amount)
                        
    #                     messages.success(request, "Transaction Completed")

    #                 debit = Debit(
    #                     card_id=gift_card,
    #                     user=merchant,
    #                     debit_amount=debit_amount,
    #                     status=status
    #                 )
    #                 debit.save()
                    

    #                 return redirect(reverse("debit_card"))
    #             except Exception as e:
                    
    #                 print("\n")
    #                 print("******************** Exception gotten in debit card ********************")
    #                 print(e)
                    
    #                 messages.error(request, "Failed to Complete Transaction")

    #                 return redirect(reverse("main:debit_card"))

    #         return render(request, "main/marchand/debit_card.html",
    #                       {
    #                           "user": merchant,
    #                       }
    #                       )
    
    # return redirect("dashboard")



def transaction(request):

    user_allowed = request.user

    if user_allowed.is_authenticated:
        if user_allowed.account_type == "0":

            # transaction

            debit = Debit.objects.all().filter(user=merchant)
            
            context = {
                "debit": debit,
                "user": user_allowed,
            }

            return render(request, "dashboard/transaction.html", context)

        elif user_allowed.account_type == "1":

            merchant = User.objects.get(id=user_allowed.id)

            debit = Debit.objects.all().filter(user=merchant)
            
            context = {
                "user": merchant,
                "debit": debit,
            }

            return render(request, "dashboard/transaction.html", context)


    return redirect("dashboard")
        

