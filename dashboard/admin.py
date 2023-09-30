from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

admin.site.register(Course)
admin.site.register(Question)
admin.site.register(QuestionResponse)
admin.site.register(QuizResult)
admin.site.register(CheckedTelegramBot)
admin.site.register(RegisteredUser)
admin.site.register(ActiveOr)
admin.site.register(Season)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    search_fields = ['name', 'phone_number']
