import os
from django.utils import timezone
from django.contrib import messages
from bridge.models import UserData
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse, FileResponse
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def landingPage(request):
    return render(request, 'bridge/landingPage.html')


@login_required
def home(request):
    return render(request, 'bridge/index.html')


@login_required
def tts(request):
    return render(request, 'bridge/tts.html')


@login_required
def stt(request):
    return render(request, 'bridge/stt.html')


@login_required
def pts(request):
    return render(request, 'bridge/pdfReader.html')


@login_required
def uploadFile(request):
    file = None
    if request.method == 'POST':
        file = upload_files(request)

    context = {
        'file': file,
    }

    return render(request, 'bridge/send.html', context)


@login_required
def upload_files(request):
    file = None
    if request.method == 'POST':
        for file in request.FILES.getlist('document'):
            fs = FileSystemStorage(location='data/')
            ext = file.name.split(".")[1].lower()
            if ' ' in str(file.name):
                return JsonResponse({'error': 'File name shouldn\'t contain any white space.'})

            if fs.exists(file.name):
                fs.delete(file.name)
            fs.save(file.name, file)
            return JsonResponse({'success': 'File Uploaded'})
    return file.name


@login_required
def check_doc(request, file_name):
    if UserData.objects.filter(fileName=file_name).exists():
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})


@login_required
def save_data(request, doc_name, no_of_pages, github_username, model, file):
    if request.method == "POST":
        print("In save data")
        print(doc_name, no_of_pages, github_username, model, file)
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        User_data = UserData(fileName=doc_name, notes=model, file=file.replace(
            ".pdf", ""), noOfPages=no_of_pages, dateTime=timezone.now(), fileOwner=user)
        User_data.save()
        User_data.user.add(user)
        user_email = user.email
        subject = 'File Saved Successfully'
        html_template = 'email/saved.html'
        text_content = 'Your file has been saved successfully.'

        context = {
            'user': user,
            'fileName': doc_name,
            'fileOwner': User_data.fileOwner,
            'notes': User_data.notes,
            'noOfPages': User_data.noOfPages,
            'dateTime': User_data.dateTime,
            'download_link': 'http://127.0.0.1:8000/bridge/preview/'
        }

        html_content = render_to_string(html_template, context)
        email = EmailMessage(subject, html_content, to=[user_email])
        email.content_subtype = "html"
        email.send()

        return JsonResponse({"file": file})


@login_required
def preview(request):
    myBooks = request.user.fileInfosOfUser.all().order_by('-dateTime')
    context = {
        'myBooks': myBooks,
    }
    return render(request, 'bridge/preview.html', context)


@login_required
def associates(request):
    print("In add collaborator")
    message_status = ""
    if request.method == 'POST':
        repo = request.POST.getlist('select_repo')
        user_email = request.POST.get('collaborator')

        if not User.objects.filter(email=user_email).exists():
            mail_subject = 'Added as a Associates!'
            password = User.objects.make_random_password()
            message = render_to_string('email/AssociatesPasswordEmail.html', {
                'repo': repo[0],
                'username': user_email,
                'password': password,
                'download_link': f'http://http://127.0.0.1:8000/bridge/preview/'
            })
            to_email = user_email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            try:
                email.send()
                print("Email Sent!")
                user = User.objects.create_user(username=user_email,
                                                email=user_email,
                                                password=password,
                                                first_name=user_email)

                repositorys = UserData.objects.get(fileName=repo[0])
                repositorys.user.add(user)
                message_status = "The given email address (" + user_email + ") has been added to the list of associates for the '" + \
                    repo[0] + "' Document. The user will receive an email notification with instructions on how to access the document."
                messages.success(request, message_status)
            except:
                print("Unable to send email. Please check if there is a typo in email.")
                message_status = "Unable to send email. Please check if there is a typo in email."
                messages.warning(request, message_status)
        elif User.objects.filter(email=user_email).exists() and user_email not in list(UserData.objects.get(fileName=repo[0]).user.all().values_list('email', flat=True)):
            mail_subject = 'Added as a Associates!'
            message = render_to_string('email/AssociatesConfirmationEmail.html', {
                'repo': repo[0],
                'download_link': 'http://127.0.0.1:8000/bridge/preview/'
            })
            to_email = user_email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            try:
                email.send()
                print("Email Sent!")
                repositorys = UserData.objects.get(fileName=repo[0])
                repositorys.user.add(
                    User.objects.filter(email=user_email)[0].id)
                message_status = "The given email address (" + user_email + ") has been added to the list of associates for the '" + \
                    repo[0] + "' Document. The user will receive an email notification with instructions on how to access the document."
                messages.success(request, message_status)
            except:
                print("Unable to send email. Please check if there is a typo in email.")
                message_status = "Unable to send email. Please check if there is a typo in email."
                messages.warning(request, message_status)
        else:
            message_status = "The email address you entered is already on the list of associates for this document."
            messages.info(request, message_status)

    repositories = UserData.objects.filter(fileOwner=request.user.id)

    repositories_associates = []
    message1 = ""
    for repo in repositories:
        if repo.user.count() > 1:
            repositories_associates.append(repo)

    if len(repositories_associates) == 0:
        message1 = "Seems like you haven't added any associates to your documents."
    print("before render")

    return render(request, 'bridge/associates.html', {'repositories': repositories, 'repositories_associates': repositories_associates, 'message1': message1})


@login_required
def removeassociates(request):
    if request.method == 'POST':
        user1 = User.objects.get(pk=request.POST["collaborator_id"])
        repo = UserData.objects.get(fileName=request.POST["documentName"])
        repo.user.remove(user1)

    return redirect('associates')


@login_required
def download_file(request, doc_name):
    print("Repo Name: ", doc_name)
    filename = doc_name + ".pdf"
    try:
        print("File Name: ", filename)
        filePath = os.path.join("data/" + filename)
        response = FileResponse(open(filePath, 'rb'))
        return response

    except:
        messages.info(request, mark_safe(
            '''
                <h5><strong>Uh Oh! Something went wrong :/</strong></h5>
                <hr>
                The file you are trying to download is either not processed because 
                zip file does not contain any  corrector output or it has been already downloaded. 
                '''
        ), extra_tags='preview_error')
        return redirect('preview')
