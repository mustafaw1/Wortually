from django.contrib import admin
from .models import (
    JobSeeker,
    OTP,
    Education,
    Language,
    JobProfileExperience,
    ApprovalModel,
    JobProfile,
    Settings,
    JobProfileAssessment,
    JobTitleAssessment,
    JobProfileInterview,
    ScreeningInterviewTemplate,
    JobProfileInterview,
    JobTitleAssessment,
    JobProfilePortfolio,
    JobProfileReview,
    JobProfileSkill,
    JobTitle
)
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('email',)


# class EducationAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Education._meta.fields] 
#     search_fields = [field.name for field in Education._meta.fields]  


# class LanguageAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Language._meta.fields]  
#     search_fields = [field.name for field in Language._meta.fields]  


# class ExperienceAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in JobProfileExperience._meta.fields]  
#     search_fields = [field.name for field in JobProfileExperience._meta.fields]  


# class ApprovalModelAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in ApprovalModel._meta.fields]  
#     search_fields = [field.name for field in ApprovalModel._meta.fields]  


# class ScreeningInterviewTemplateAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in ScreeningInterviewTemplate._meta.fields]  
#     search_fields = [field.name for field in ScreeningInterviewTemplate._meta.fields]  
#     exclude = ("added_by",)

#     def save_model(self, request, obj, form, change):
#         if not obj.pk:  # If the object is being created
#             obj.added_by = request.user  # Assign the logged-in user to added_by
#         super().save_model(request, obj, form, change)

#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         if not request.user.is_superuser:
#             form.base_fields["added_by"].queryset = User.objects.filter(
#                 pk=request.user.pk
#             )
#         return form

#     def has_add_permission(self, request):
#         return request.user.is_superuser

#     def has_change_permission(self, request, obj=None):
#         return request.user.is_superuser

admin.site.register(JobProfile)
admin.site.register(Education)
admin.site.register(Language)
admin.site.register(JobProfileExperience)
admin.site.register(ApprovalModel)
admin.site.register(Settings)
admin.site.register(JobTitleAssessment)
admin.site.register(JobProfileInterview)
admin.site.register(JobProfileAssessment)
admin.site.register(ScreeningInterviewTemplate)
admin.site.register(OTP)
admin.site.register(JobProfilePortfolio)
admin.site.register(JobProfileSkill)
admin.site.register(JobTitle)
admin.site.register(JobProfileReview)