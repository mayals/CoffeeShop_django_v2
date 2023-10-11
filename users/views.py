from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model 
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from .models import UserProfile
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm




def signup_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user.set_password(password)
            user.is_confirmEmail = False
            user.is_active = False
            user.save()
            form = UserRegisterForm()
            messages.success(request, f'thanks ({user.first_name}), please complete registeration by confirm Your Email Address:({user.email}) message')
            return redirect('users:signin')
            # NOW AFTER A NEW user IS CREATED IN DATABASE, THEY ARE 3 SIGNALS, users.signals WILL WORK automatically:
            #1 SEGNAL GO TO CREATE TOKEN AND SEND  configuration link TO THE ABOVE EMAIL FOR EMAIL CONFIGRATION
            #2 SIGNAL GO TO WORK CREATE PROFILE OBJECT FOR THIS USER WAS CREATED
            #3 SEGNAL GO TO CREATE OTP CODE AND SEND IT TO  MOBILE AS SMS MESSAGE FOR PHONE NUMBER CONFIGRATION
            # user can't login until he go to his email and link confirmed.
    else:
        form = UserRegisterForm()

    #---- register context -------
    context = {
        'title' : "Register Page",
        'form' : form ,
    }    
    return render(request,'users/signup.html', context)









# check before login - work after the email reach to user and he clik the link inside it 
###################### EmailConfirmAPIView #################
def confirmEmail_and_activateUser(request,uidb64,token):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return HttpResponse('User does not exit!')

        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.is_confirmEmail = True
            user.save()
            
            #user = authenticate(request, email=email, password=password)
            login(request,user)
            messages.success(request, 'Conguratulation ( {} ) you do success Registration and login, please edit your profile'.format(user.email))
            userprofile = get_object_or_404(UserProfile, user=user)
            return redirect('users:edit-profile',prof_id=userprofile.id)
            #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')




def signin_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        email    = request.POST['email']  
        password = request.POST['password'] 
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active == True & user.is_confirmEmail == True :
                login(request,user)
                form = UserLoginForm()
                messages.success(request,'you do success login.')
                return redirect('pages:index')
                #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
                form = UserLoginForm()
                messages.info(request,f'Before login you must open your email and confirm email message')
        
    else:
        form = UserLoginForm()        
    context = {
        'title' : "Signin Page",  
        'form' : form ,        
    }    
    return render(request,'users/signin.html', context)




@login_required(login_url='users:signin')
def signout_view(request):
    logout(request)
    return redirect('pages:index')



@login_required(login_url='users:signin')
def profile_view(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    context ={
        'title': 'Profile page',
        'profile': profile ,
    }
    return render(request,'users/profile.html', context)






@login_required(login_url='users:signin')
def edit_profile_view(request,prof_id):
    user = request.user
    profile = get_object_or_404(UserProfile,id=prof_id,user=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.user = request.user
            profile.id = prof_id
            profile.save()
            messages.success(request, f'thanks ( {request.user.first_name} ), your profile edit successfully !')
            return redirect('users:profile-view')
    else:
        form = UserProfileForm(instance=profile)      
    
    context = {
       'title' : "Profile Page",
       'form'  : form,
        
    }    
    return render(request,'users/edit_profile.html', context)   
