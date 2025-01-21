from django.shortcuts import redirect, render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth
# Create your views here.

class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        username=data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should only contain alphanumeric characters'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Sorry! The username already exists. Please choose another one.'},status=409)
        return JsonResponse({'username_valid':True})

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})

class RegisterationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    def post(self,request):
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]

        context={
            'fieldValue': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request,"Password is too short!")
                    return render(request,'authentication/register.html',context)
                else:
                    user=User.objects.create_user(username=username,email=email)
                    user.set_password(password)
                    user.is_active= False
                    user.save()

                    uid = urlsafe_base64_encode(force_bytes(user.pk))

                    domain = get_current_site(request).domain
                    link= reverse('activate',kwargs={'uid': uid , 'token':token_generator.make_token(user)})

                    activate_url = f'http://{domain}{link}'
                    email_subject = "Activate your account!"
                    email_body = "Hey " +user.username + "\n Please use link to activate your account \n" + "http://"+ activate_url
                    email = EmailMessage(
                        email_subject,
                        email_body,
                        "noreply@semicolon.com",
                        [email],
                    )
                    email.send(fail_silently=False)
                    messages.success(request,"User created successfully")
                    return render(request,'authentication/register.html')


        return render(request,'authentication/register.html')
    
class VerficationView(View):
    def get(self, request, uid, token):
        try:
            id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                messages.error(request, "Invalid or expired activation link.")
                return redirect('login')

            if user.is_active:
                messages.info(request, "Your account is already activated.")
                return redirect('login')
            

            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')



class LoginView(View):
    def get(self, request):
        return render(request,'authentication/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "Welcome "+user.username+" you are now logged in successfully!")
                    return redirect('expenses')
                messages.error(request, "Your account is not activated yet, check you email!")
                return render(request,'authentication/login.html')
            messages.error(request, "Invalid credentials, try again!")
            return render(request,'authentication/login.html')
        
        messages.error(request, "Please fill all the fields!")
        return render(request,'authentication/login.html')
    
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You are now logged out successfully!")
        return redirect('login')