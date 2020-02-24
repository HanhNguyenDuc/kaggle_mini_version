from django.shortcuts import render
from django.views import View
from django.template.loader import get_template
from django.http import HttpResponse
from .models import Member, Contest, Relationship, Submission
from django.contrib.auth import decorators, login
from django.http import HttpResponseRedirect
from .forms import UploadFileForm, ModelFormWithFileField, SubmissionForm, MemberCreationUIForm, LoginForm
import pandas as pd
from django.db.models import Max
# Create your views here.

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'home/login.html', {'form': form})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        
        return render(request, 'home/login.html', {'form': form})


@decorators.login_required(login_url='/login/')
def get_all_contests():
    # return contest_name and contest_url
    contests = Contest.objects.all()
    res = []
    for contest in contests:
        tmp_contest = {}
        tmp_contest.update({'name': contest.name})
        tmp_contest.update({'url': '/home/contest/{}'.format(contest.id)})
        res.append(tmp_contest)
    
    return res


class RegisterView(View):
    def get(self, request):
        form = MemberCreationUIForm()
        template = get_template('home/registration.html')
        return HttpResponse(template.render({'form': form}, request))

    def post(self, request):
        form = MemberCreationUIForm(request.POST)
        if form.is_valid():
            form.save()
            print('Member has been saved')
            return HttpResponseRedirect('/home/login')
        else:
            print('form is not valid')

        return HttpResponse(render(request, 'home/registration.html', {'form': form}))


@decorators.login_required(login_url='/login/')
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
    return_dict.update({'list_contest': get_all_contests()})
    
    template = get_template('home/home.html')


    print(return_dict)
    return HttpResponse(template.render(return_dict, request))

@decorators.login_required(login_url='/login/')
def get_contest_page(request):
    template = get_template('home/contest.html')
    return HttpResponse(template.render({}, request))


@decorators.login_required(login_url='/login/')
def get_info_page(request):
    template = get_template('home/info.html')
    return HttpResponse(template.render({}, request))


@decorators.login_required(login_url='/login')
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

@decorators.login_required(login_url = "/login/")
def get_contest(request, id = 1):
    if request.method == 'POST':
        data = {}
        contest = Contest.objects.get(id=id)
        user = request.user
        form = SubmissionForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid:
            submit_file = request.FILES['file']
            max_size = 102400
            if submit_file.size > max_size:
                data['server_msg'] = "Your submission is denied. Error 01"
            elif submit_file.name.split('.')[-1] not in ['csv']:
                data['server_msg'] = "Your submission is denied. Error 02"
            submission_id = None
            try:
                submission = Submission(file=submit_file, member=user, contest=contest)
                submission.save()
                submission_id = Submission.objects.count()
                data['server_msg'] = "Submit sucessfully"

            except Exception as e:
                data['server_msg'] = "Error while interacting with database {}".format(e)

            solution_file = contest.solution_file.file
            df = pd.read_csv(solution_file)
            result_dict = df.set_index('ImageID')['Label'].to_dict()
            # print(result_dict)
            try:
                submission = Submission.objects.get(id=submission_id)
                sub_file = submission.file
                df = pd.read_csv(sub_file)
                sub_dict = df.set_index('ImageID')['Label'].to_dict()
                # print(sub_dict)
                total_c = 0
                good_pred = 0
                for key in result_dict:
                    total_c += 1
                    try:
                        if result_dict[key] == sub_dict[key]:
                            good_pred += 1
                    except:
                        data['server_msg'] = "File submitted has wrong format"
                score = good_pred/total_c
                submission.score = score
                submission.save()
                data['server_msg'] = "Last submission has result: {}".format(score)
            except Exception as e:
                print(e)
                data['server_msg'] = "File submitted is illegal"
            print(data['server_msg'])
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
    content.update({'id': id})

    contest = Contest.objects.get(id=id)
    submissions = Submission.objects.filter(contest=contest)
    submission_content = []
    for key, submission in enumerate(submissions):
        tmp_content = {}
        tmp_content.update({'order': key})
        tmp_content.update({'first_name': submission.member.first_name})
        tmp_content.update({'last_name': submission.member.last_name})
        tmp_content.update({'score': submission.score})
        tmp_content.update({'file_size': submission.file.size})
        tmp_content.update({'date': submission.date})
        submission_content.append(tmp_content)

    member_list = Member.objects.all()
    rank_list = []
    counter = 0
    for member in member_list:
        sub_list = Submission.objects.filter(member=member)
        highest_score = sub_list.aggregate(Max('score'))['score__max']
        if highest_score:
            counter += 1
            tmp_rank = {}
            tmp_rank.update({'order': key})
            tmp_rank.update({'first_name': member.first_name})
            tmp_rank.update({'last_name': member.last_name})
            tmp_rank.update({'score': highest_score})
            rank_list.append(tmp_rank)

    return render(
        request, 
        'home/contest.html', 
        {
            'form': form, 
            'content': content, 
            'list_contest': get_all_contests(),
            'submission_content': submission_content,
            'rank_content': rank_list,
        }
    )

@decorators.login_required(login_url="/login")
def get_submission_page(request, id=1):
    contest = Contest.objects.get(id=id)
    submissions = Submission.objects.filter(contest=contest)
    content = []
    for submission in submissions:
        tmp_content = {}
        tmp_content.update({'first_name': submission.member.first_name})
        tmp_content.update({'last_name': submission.member.last_name})
        tmp_content.update({'score': submission.score})
        content.append(tmp_content)
    
    
    return render(
        request, 
        'home/submissions.html', 
        {
            'content': content, 
            'list_contest': get_all_contests()
        }
    )



