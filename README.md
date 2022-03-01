# Ethikdo #


## App test for Ethikdo ## 


## Introduction ##
This document provides the instructions for using the Ethikdo Application developed by Dieuveille BOUSSA ELLENGA. 
This (partial) application made for Ethikdo is used to manage gift cards. 


### Definition ###

The app is based on the CRUD user interface convention.  

Create: you can add : new user instances (with different roles) /   new gift cards 
Read: you can access those user instances (see the names, usernames, emails …) / the gifts cards (title, slug, amount, ...) 
Update: you can edit the users, change the name, username, type of user ...  
Delete: you can also delete users, but it is advised not to, instead turn them inactive by unchecking the active field for that user on the Django Admin panel. 


### Target audience ###

This document is targeted (but not limited) to technical individual with a Web Development (Django) background 


**************************************** ReadMe ****************************************

***** Liens Utiles

	*** Accueil Visiteurs    178.0.0.1:8000

	*** Accueil Marchands    178.0.0.1:8000/marchand

	*** Accueil Admins       178.0.0.1:8000/admin_home


***** Fonctions

créer un nouvel utilisateur : commerçant et Admin

Se connecter
 

Admin peut créer un un nouvel utilisateur comerçant

Admin peut créer une carte en indiquant le montant ( le code / numero de la carte est généré automatiquement )

Admin peut débiter ou créditer une carte

Admin peut voir toutes les cartes

Admin peut voir tous les utilisateurs marchands

Admin peut voir toutes les transactions 


Marchand peut débiter une carte



**************************************** ReadMe ****************************************

 



# Document #




 



# Application components #
There are two ways to use the Account Module:  

Starting a fresh new project and integrating the module in it    

Using the module’s project as base and add other modules in it   


## 3.1 Starting New Project ##   

As a complementary module, the Account Module must be integrated in another project / website. 

**Attention** it is advised that this module be integrated before creating a user for your project, else, you will encounter a database migration issue (which you can still solve, but it is untoward)  

After starting a new project i.e. django-admin startproject mysite (mysite being the name of the project) we access the new directory mysite, and open the mysite folder  

We will modify two files, settings.py and urls.py, but first we copy the account module and the dashboard module to our main folder. 

We then open our IDE / text editor to edit the files. 


**In setting.py:**  mysite/settings.py  

In INSTALLED_APPS (~line 33) we comment the ‘django.contrib.admin’ line and we add two lines ‘account’, and ‘dashboard’, to register the two new apps to the project 

  And we add AUTH_USER_MODEL = "account.User" after ALLOWED_HOSTS


**In urls.py:**  mysite/urls.py 

In urlpattern (~line 20) we comment the path(‘admin/’, admin.site.urls),  

And we also comment the from django.contrib import admin line  

Then, we run the migrations. 

After running the migrations, we create a superuser and we can uncomment everything we commented and run the migrations again.  

We now register the urls of our new apps, by importing include after path  

from django.urls import path, include  

and adding two new lines in urlpatterns   

path('account/', include('account.urls')), 

path('', include('dashboard.urls')), 


We add the static root, media root, template path in the settings.py and urls.py files. 
Then, we create one and only one instance of the allow_registration models from the django admin panel or using our terminal 


Cmd -> python ->  

import os 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  

from django.core.wsgi import get_wsgi_application 

application = get_wsgi_application() 

from account.models import *   

allow = AllowRegistration(name='user_registration', status=True)   

allow.save() 


Basics functionalities have been implemented: Login, Logout, Register, Edit Profile, Change Password, Reset or Recover Password. 

**Attention** the Registration view depends on the Admin, there is a functionality Allow_Registration which may (or may not) allow new users to register. 
The Admin must login and choose if people can register or not to the website, it can be changed on the dashboard or on the Django admin panel and it is set to True by default, meaning users can register to the web application.  


**In setting.py:** mysite/settings.py we add the following at the bottom of the page 

LOGIN_REDIRECT_URL = 'dashboard' 

LOGIN_URL = 'login' 

LOGOUT_URL = 'logout' 

LOGOUT_REDIRECT_URL = 'login' 

AUTHENTICATION_BACKENDS = [ 

    'django.contrib.auth.backends.ModelBackend', 

    'account.authentication.EmailAuthBackend' 

] 

This tells our application where to redirect the user after logging in and logging out and allows the users to also be able to login with their address email and password as well as username and password.  

And, so far, our project is up and running.  


## 3.2 Using Account Module as Base ## 

We clone the specific repository or download the compressed project; the project contains the Account module and the Dashboard module. 
The project has been dockerized (the docker-compose.yml may be changed according to the need of the project you are building), so we start by building the environment by running docker-compose build then docker-compose up  

This should also run the migrations, we can now create a super user and take a look at the app.  

By default, we have created 4 types of users: type1, type2, type3 and type4, the names can be changed in the models.py file (after every change, we must run the migrations, restarting docker works too).  

The Dashboard app has only one view redirected after we have logged in.

Basics functionalities have been implemented: Login, Logout, Register, Edit Profile, Change Password, Reset or Recover Password. 

**Attention** the Registration view depends on the Admin, there is a functionality Allow_Registration which may (or may not) allow new users to register. 
The Admin must login and choose if people can register or not to the website, it can be changed on the dashboard or on the Django admin panel and it is set to True by default, meaning users can register to the web application.  

The desired project can then be built around those modules and the different type of users can be given roles.



## 3.3 Password Reset Server Configuration ## 

**In setting.py:** mysite/settings.py  




