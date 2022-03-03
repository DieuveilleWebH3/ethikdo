from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    # 
    path('', views.dashboard, name='dashboard'),
    
    #
    # path('admin/home', views.dashboard_admin, name='dashboard_admin'),
    
    #
    # path('admin/home', views.dashboard_admin, name='dashboard_admin'),
    
    
    # path('add/card', views.add_card, name="add_card"),
    
    path('manage/card/', views.manage_card, name="manage_card"),
    
    # path('manage/users', views.manage_users, name="manage_users"),
    
    # path('manage/transaction', views.manage_transaction, name="manage_transaction"),
    
    # path('topup/card', views.top_up_card, name="top_up_card"),


    # path('contact', views.contact, name="contact"),

    # path('check_gift_card_exist', views.check_gift_card_exist, name="check_gift_card_exist"),
    
    # path('debit/card', views.debit_card, name="debit_card"),

    # path('transaction', views.transaction, name="transaction"),
    
]
