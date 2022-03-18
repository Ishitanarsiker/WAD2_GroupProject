from django.shortcuts import render, redirect
from django.urls import reverse
from lectureFinderApp.models import Lecture
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

def signup_user(request):
	return render(request,'lectureFinderApp/index.html',{"form":UserCreationForm})

def login_user(request):
		if request.method == "POST":
			username = request.POST['uname']
			password = request.POST['pass']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request,user)
					return redirect('home')
				else:
					return render(request, 'index.html', {'error_message':'Account Deactivaated'})
			else:
				return render(request, 'index.html', {'error_message':'Invalid Login'})
		return render(request, 'lectureFinderApp/login_user.html')

def about(request):
	return render(request, 'lectureFinderApp/about.html')

def termsandconditions(request):
	return render(request, 'lectureFinderApp/termsandconditions.html')

# @login_required
def members(request):
	test_user_luke = User.objects.get(first_name="Luke")

	# TODO: Uncomment the below (and delete the line above), when authentication system complete
	# logged_in_user = User.objects.get(user_id=request.user.id)
	# logged_in_user = UserProfile.objects.get(user=logged_in_user)

	logged_in_user = UserProfile.objects.get(user=test_user_luke)
	all_saved_lectures_for_user = SavedLecture.objects.all().filter(user=logged_in_user)

	context_dict = {
		'saved_lectures': all_saved_lectures_for_user
	}

	return render(request, 'lectureFinderApp/members.html', context=context_dict)


def search(request):
	return render(request, 'lectureFinderApp/search.html')


def show_lecture(request, lecture_name_slug):
	context_dict = {}
	lecture_to_show = Lecture.objects.get(slug=lecture_name_slug)

	context_dict['lecture'] = lecture_to_show

	return render(request, 'lectureFinderApp/show_lecture.html', context=context_dict)


@login_required
def save_lecture(request, lecture_name_slug):
	current_user = UserProfile.objects.get(user=User.objects.get(user_id=request.user.id))

	if request.method == 'POST':
		saved_leture = SavedLecture.objects.create(
			lecture=Lecture.objects.get(slug=lecture_name_slug),
			user=current_user
		)

	return redirect(reverse('lectureFinderApp:search'))


@login_required
def remove_saved_lecture(request, lecture_name_slug):
	current_user = UserProfile.objects.get(user=User.objects.get(user_id=request.user.id))

	if request.method == 'POST':
		saved_leture = SavedLecture.objects.delete(
			lecture=Lecture.objects.get(slug=lecture_name_slug),
			user=current_user
		)

	return redirect(reverse('lectureFinderApp:members'))

def signup(request):
	signup = False

	if request.method == 'POST':
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture'] 

			profile.save()

			signup = True 
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request,
		          'lectureFinderApp/signup.html',
		          context = {'user_form': user_form,
		                     'profile_form': profile_form,
		                     'signup': signup})

