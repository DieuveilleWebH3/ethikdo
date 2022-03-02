from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    # 
    path('', views.dashboard, name='dashboard'),
    
    
    # path('add_card', admin_views.add_card, name="add_card"),
    
    # path('manage_card', admin_views.manage_card, name="manage_card"),
    
    # path('manage_marchand', admin_views.manage_marchand, name="manage_marchand"),
    
    # path('manage_transaction', admin_views.manage_transaction, name="manage_transaction"),
    
    # path('top_up_card', admin_views.top_up_card, name="top_up_card"),


    # path('contact', views.contact, name="contact"),

    # path('check_gift_card_exist', views.check_gift_card_exist, name="check_gift_card_exist"),
    
    # path('debiter', views.debit_card, name="debit_card"),

    # path('transaction', views.transaction, name="transaction"),
    
]
