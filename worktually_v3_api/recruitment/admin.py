from django.contrib import admin

from recruitment.models import *

admin.site.register(JobApplication)
admin.site.register(JobPost)
admin.site.register(JobOffer)
admin.site.register(Candidate)
admin.site.register(JobInterview)
admin.site.register(APIKey)
