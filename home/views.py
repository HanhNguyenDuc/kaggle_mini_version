from django.shortcuts import render
from django.views import View
from django.template.loader import get_template
from django.http import HttpResponse
from .models import Member, Contest, Relationship, Submission
from django.contrib.auth import decorators
from django.http import HttpResponseRedirect
from .forms import UploadFileForm, ModelFormWithFileField, SubmissionForm
# Create your views here.

class RegisterView(View):
    def get(self, request):
        template = get_template('home/registration.html')
        return HttpResponse(template.render({}, request))

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']

        template = get_template('home/redirect.html')

        member = Member(username=username, password=password, email=email, first_name=firstname, last_name=lastname)
        member.save()

        return HttpResponse(template.render({}, request))


@decorators.login_required(login_url='/home/login/')
def get_home_page(request):
    contest_list= list(Contest.objects.all())
    print(vars(contest_list[0]))
    return_dict = {}
    list_contest = []
    for contest in contest_list:
        content = {}
        content.update({'name': contest.name})
        content.update({'max_score': contest.max_score})
        content.update({'description': contest.description})
        content.update({'data_path': contest.data_path})
        content.update({'img_url': contest.represent_image})
        content.update({'contest_id': contest.id})
        list_contest.append(content)

    return_dict.update({'list_content': list_contest})
    
    template = get_template('home/home.html')
    print(return_dict)
    return HttpResponse(template.render(return_dict, request))

@decorators.login_required(login_url='/home/login/')
def get_contest_page(request):
    template = get_template('home/contest.html')
    return HttpResponse(template.render({}, request))


@decorators.login_required(login_url='/home/login/')
def get_info_page(request):
    template = get_template('home/info.html')
    return HttpResponse(template.render({}, request))


@decorators.login_required(login_url='/home/login')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES)
            return HttpResponseRedirect('/home')
    else:
        form = UploadFileForm()

    return render(request, 'home/upload.html', {'form': form})


def handle_uploaded_file(f):
    with open('name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)



def upload_file_2(request):
    if request.method == 'POST':
        form = ModelFormWithFileField(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid:
            # save file
            form.save()
            return HttpResponseRedirect('/home')
    else:
        form = ModelFormWithFileField()
        
    return render(request, 'home/upload.html', {'form': form})

@decorators.login_required(login_url = "home/login")
def get_contest(request, id = 1):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid:
            
            submission = Submission(file=request.FILES['file'])
            submission.save()
            return HttpResponseRedirect('/home/contest/{}'.format(id))
    else:
        form = SubmissionForm()
    
    contest = Contest.objects.filter(id = id)[0]

    content = {}
    content.update({'name': contest.name})
    content.update({'max_score': contest.max_score})
    content.update({'description': contest.description})
    content.update({'data_path': contest.data_path})
    content.update({'img_url': contest.represent_image})

    return render(request, 'home/contest.html', {'form': form, 'content': content})


