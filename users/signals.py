from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from coffeeshop.settings import DEFAULT_FROM_EMAIL
from .models import UserModel, SMSCode, UserProfile
# https://pypi.org/project/django-rest-passwordreset/
# https://github.com/anexia-it/django-rest-passwordreset/blob/master/README.md#example-for-sending-an-e-mail
# from django_rest_passwordreset.signals import reset_password_token_created      

# https://pypi.org/project/python-dotenv/
#load_dotenv()  # take environment variables from .env.
from dotenv import load_dotenv


load_dotenv() # to load environment variables DEFAULT_FROM_EMAIL from .env file


# signal-1
# sender   =   get_user_model()        -------- from django.contrib.auth import get_user_model
# receiver =   def send_confirmation_email  ---------------- to send email message that told the new registered user that Email Confirmation is done correctly
@receiver(post_save, sender=UserModel, dispatch_uid="unique_identifier")
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        try:
            subject = 'Confirm Your Email Address'
            message = render_to_string('users/email_confirmation.html', 
                                                    {
                                                    'user': instance,
                                                    'domain': 'localhost:8000',
                                                    'uid': urlsafe_base64_encode(smart_bytes(instance.pk)),
                                                    'token': default_token_generator.make_token(instance),
                                                    }
            ) 
            from_email = DEFAULT_FROM_EMAIL    # load_dotenv() - this work her to bring this variable value from file .env
            to_email = instance.email
            send_mail(subject, message, from_email, [to_email], fail_silently=False)
        except Exception as e:
            print(f'Error sending confirmation email: {e}')




#signal-2
# sender   =   get_user_model()            -------- from django.contrib.auth import get_user_model
# receiver =   create_user_profile         --------  to creat new UserProfile in database table for the new registerd user 
@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
            UserProfile.objects.create(user=instance)
            

# another way of writing the above signal code 
# def create_user_profile(sender, **kwarg):
#     if kwarg['created']:
#        UserProfile.objects.create(user=kwarg['instance'])

# # signal
# post_save.connect(create_user_profile, sender=get_user_model())





#signal-3
# sender   =   get_user_model()                -------- from django.contrib.auth import get_user_model
# receiver =  post_save_generate_code          -------- to creat new OTP code in database table for the new registerd user 
@receiver(post_save, sender=get_user_model())
def post_save_generate_code(sender, instance, created, *args, **kwargs):
    if created:
            SMSCode.objects.create(user=instance)









############################# By using   # https://pypi.org/project/django-rest-passwordreset/ #########################################

# sender   =   reset_password_token_created   -------- from django_rest_passwordreset.signals import reset_password_token_created
# receiver =   password_reset_token_created  ---   to send email message that told the user that password_reset_token_created  is done correctly
# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     """
#     Handles password reset tokens. Sends an email to the user when a token is created.
#     """
#     context = {
#         'current_user': reset_password_token.user,
#         'first_name': reset_password_token.user.first_name,
#         'email': reset_password_token.user.email,
#         'reset_password_url': f"{instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm'))}?token={reset_password_token.key}"
#     }

#     email_html_message = render_to_string('api/v1/users/reset_password.html', context)

#     subject = "Password Reset for BookStoreAPI Account"
#     from_email = DEFAULT_FROM_EMAIL
#     to_email = reset_password_token.user.email
    
#     msg = EmailMultiAlternatives(subject, email_html_message, from_email, [to_email])
#     # msg.attach_alternative(email_html_message, "text/html")
#     msg.send()