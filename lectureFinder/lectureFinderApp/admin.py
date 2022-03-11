from django.contrib import admin
from lectureFinderApp.models import UserProfile, Course, Lecture, SavedLecture

# Register your models here.
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(SavedLecture)
admin.site.register(UserProfile)
