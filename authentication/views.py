from django.contrib import messages
from django.shortcuts import render
from .forms import Registration_Form
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

UserModel = get_user_model()

# Create your views here.


def register(request):
    emp_register = Registration_Form()
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == "POST":
        register = Registration_Form(request.POST)
        if register.is_valid():
            user = register.save()
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('email/email_body.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = request.POST['email']
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            try:
                email.send()
            except Exception as e:
                print("Error in Registration: ", e)
                messages.error(
                    request, 'Unable to send email. Please check if there is a typo in email.')
                return render(request, 'authentication/register.html', {'register': emp_register})

            messages.success(
                request, "We've emailed you instructions for verifying your account. If they haven't arrived in a few minutes, check your spam folder.")
            return HttpResponseRedirect('/bridge/accounts/login/')
        else:
            return render(request, "authentication/register.html", {'register': register})
    return render(request, "authentication/register.html", {'register': emp_register})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, "You are verified and registered successfully!")
        return HttpResponseRedirect('/bridge/accounts/login/')
    else:
        return HttpResponse("Invalid Link!")
