from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Inquiry

def inquiry(request):
   if request.method == 'POST':
       listing_id = request.POST['listing_id']
       listing = request.POST['listing_id']
       name = request.POST['name']
       email = request.POST['email']
       phone = request.POST['phone']
       message = request.POST['message']
       user_id = request.POST['user_id']
       realtor_email = request.POST['realtor_email']

       if request.user.is_authenticated:
           user_id = request.user.id 
           has_contacted = Inquiry.objects.all().filter(listing_id=listing_id, user_id=user_id)
           if has_contacted:
               messages.error(request, 'You have already made an inquiry!')
               return redirect('/listings/'+listing_id)
       
       inquiry = Inquiry(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)

       inquiry.save()

       send_mail(

           'Property Listing Inquiry',
           'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info',
           'imdonfrancis@gmail.com',
           [realtor_email,'imjulianevillafuerte@gmail.com'],
           fail_silently=False

       )

       messages.success(request, 'Your request has been submitted, We will get back to you soon')
       return redirect('/listings/'+listing_id)
