from django.contrib import admin
from .models import Member, Relationship, Contest, Submission
from django.contrib.auth.admin import UserAdmin

from .forms import MemberChangeForm, MemberCreationForm
# from .models import Member
# Register your models here.

class MemberAdmin(UserAdmin):
    add_form = MemberCreationForm
    form = MemberChangeForm
    model = Member
    list_display = ['email', 'username']

admin.site.register(Member, MemberAdmin)
admin.site.register(Contest)
admin.site.register(Relationship)
admin.site.register(Submission)



