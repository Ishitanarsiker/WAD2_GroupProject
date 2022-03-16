from django.contrib import admin
from lectureFinderApp.models import UserProfile, Course, Lecture, SavedLecture


class LectureAdmin(admin.ModelAdmin):
	list_display = ('title', 'course', 'professor')


# Register your models here.
admin.site.register(Course)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(SavedLecture)
admin.site.register(UserProfile)
