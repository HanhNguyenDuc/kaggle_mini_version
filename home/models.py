from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# from django.db import models

# Create your models here.
class Member(AbstractUser):
    first_name = models.CharField(name="First Name", default="username_first", max_length=100)
    last_name = models.CharField(name="Last Name", default="username_last", max_length=100)
    # total_score = models.CharField(name="Score", default="total_score", max_length=100)/
    total_contribute = models.FloatField(name="contribute", default=0)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Contest(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    name = models.CharField(name="name", default="contest_x", max_length=100)
    data_path = models.CharField(name="data_path", default="/", max_length=100)
    max_score = models.IntegerField(name="max_score", default=100)
    description = models.CharField(name="description", default="Empty", max_length=1000)
    data_required = models.BooleanField(name="data_require", default=True)
    represent_image = models.CharField(name="represent_image", default="/", max_length=100)
    solution_file = models.FileField(name="solution_file", default=None)
    

    # def __str__(self):
    #     return self.data_path

class Relationship(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    score = models.FloatField(name="score", default=0)


    def __str__(self):
        return '{}-{}'.format(self.member, self.contest)

class FileModel(models.Model):
    file_name = models.CharField(name = "file_name", default="file_name", max_length=100)
    file = models.FileField(name="file")
    datetime = models.DateField(name="datetime", null=True)

class Submission(models.Model):
    id = models.IntegerField(name="id", auto_created=True, primary_key=True)
    member = models.ForeignKey(Member, name="member", on_delete=models.CASCADE, default=None)
    contest = models.ForeignKey(Contest, name="contest", on_delete=models.CASCADE, default=None)
    file = models.FileField(name="file")
    date = models.DateField(name="date", auto_now=True)
    score = models.FloatField(name="score", default=0)
    

    

    