from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Member, FileModel, Contest, Submission
import datetime

class MemberCreationForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ('username', 'email')


class MemberChangeForm(UserChangeForm):
    class Meta:
        model = Member
        fields = ('username', 'email')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class ModelFormWithFileField(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ['file_name', 'file', 'datetime']
        widgets = {
            'datetime': forms.DateTimeInput(),
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('file', )
    
    # def save(self):
    #     submit = super(SubmissionForm, self).save(commit=False)
    #     submit.date = datetime.date.day()
    #     submit.score = 0

    #     submit.save()
    



        