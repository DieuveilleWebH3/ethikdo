# Ethikdo #


## App test for Ethikdo ## 


## Introduction ##
This document provides the instructions for using the Ethikdo Application developed by Dieuveille BOUSSA ELLENGA. 
This (partial) application made for Ethikdo is used to manage gift cards. 


### Definition ###

The app is based on the CRUD user interface convention.  

**Create:** you can add : new user instances (with different roles) /   new gift cards 

**Read:** you can access those user instances (see the names, usernames, emails …) / the gifts cards (title ?, slug ?, amount, ...) 

**Update:** you can edit the users, / gift cards (top up , debit) ...  

**Delete:** you can also delete users (but it is advised not to, instead turn them inactive by unchecking the active field for that user on the Django Admin panel) / gift cards 



### Target audience ###

This document is targeted (but not limited) to technical individual with a Web Development (Django) background 



## Application components ##

There are two 2 components in this project
 - The Account Module

 - The Gift cards management   




**Useful Links**

 - Django Admin Panel   178.0.0.1:8009/admin/myadmin

 - Homepage             178.0.0.1:8009

 - Homepage Merchant    178.0.0.1:8009/marchant/home

 - Homepage Admin       178.0.0.1:8009/admin/home


**Functions**

register : create new users (Merchant & Admin)

activate account 

login
 

Admin can create new gift cards (amount, auto generated code/number, title ?, slug?)

Admin can debit or topup cards 

Admin can see all cards

Admin can see all users

Admin can see all transactions 



Marchant can debit cards  

