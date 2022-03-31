from django.contrib import admin
from django.db import models
from utils import AdminImageWidget

from .models import User, UserProfile, Course, Student, Announcement, Quiz, \
    Question, Answer, Tutorial, Notes, Instructor, TakenQuiz, StudentAnswer, Campus, Department, Specialization
from django.utils.safestring import mark_safe


# Register your models here.
admin.site.register(User)
# admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Announcement)
admin.site.register(Answer)
admin.site.register(Tutorial)
admin.site.register(Notes)
admin.site.register(Instructor)
admin.site.register(TakenQuiz)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(StudentAnswer)
admin.site.register(Campus)
admin.site.register(Department)
admin.site.register(Specialization)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    readonly_fields = ['image_preview'] 
    formfield_overrides = {models.ImageField: {'widget':AdminImageWidget}}


    # ------ Image Preview Start ------
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='150' height='150' style='object-fit:contain' />")
        else:
            return 'No Image'
    image_preview.short_description = 'Image Preview' 
    image_preview.allow_tags = True
    # ------ Image Preview End ------
