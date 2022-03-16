from django.shortcuts import render
from django.urls import reverse
from lectureFinderApp.models import Lecture, SavedLecture, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
	# Index page will display both the recently uploaded and the most viewed lectures.
	all_lectures = Lecture.objects.all()  # ordered by last record inserted into the table.
	all_lectures_by_views = all_lectures.order_by('-views')

	context_dict = {
		'recently_uploaded': all_lectures,
		'most_viewed': all_lectures_by_views
	}

	return render(request, 'lectureFinderApp/index.html', context=context_dict)


def about(request):
	return render(request, 'lectureFinderApp/about.html')


@login_required
def members(request):
	# When login system complete, can replace test code below with request.user.id etc.
	test_user_luke = User.objects.get(first_name="Luke")
	logged_in_user = UserProfile.objects.get(user=test_user_luke)
	all_saved_lectures_for_user = SavedLecture.objects.all().filter(user=logged_in_user)

	context_dict = {
		'saved_lectures': all_saved_lectures_for_user
	}

	return render(request, 'lectureFinderApp/members.html', context=context_dict)


def search(request):
	return render(request, 'lectureFinderApp/search.html')


def about(request):
	return render(request, 'lectureFinderApp/about.html')


def show_lecture(request, lecture_name_slug):
	return render(request, 'lectureFinderApp/show_lecture.html')
