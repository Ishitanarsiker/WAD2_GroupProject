from django.shortcuts import render, redirect
from django.urls import reverse
from lectureFinderApp.models import Lecture, SavedLecture, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, UserProfileForm


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


def terms_and_conditions(request):
    return render(request, 'lectureFinderApp/terms_and_conditions.html')


@login_required
def members(request):
    logged_in_user = User.objects.get(id=request.user.id)
    logged_in_user = UserProfile.objects.get(user=logged_in_user)
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
    current_user = UserProfile.objects.get(user=User.objects.get(id=request.user.id))

    saved_lecture = SavedLecture.objects.create(
        lecture=Lecture.objects.get(slug=lecture_name_slug),
        user=current_user
    )
    saved_lecture.save()

    return redirect(reverse('lectureFinderApp:index'))


@login_required
def remove_saved_lecture(request, lecture_name_slug):
    current_user = UserProfile.objects.get(user=User.objects.get(id=request.user.id))
    saved_lecture = SavedLecture.objects.delete(
        lecture=Lecture.objects.get(slug=lecture_name_slug),
        user=current_user
    )

    return redirect(reverse('lectureFinderApp:members'))


def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = user_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect(reverse('lectureFinderApp:members'))
        else:
            print(user_form.errors, user_profile_form.errors)
            return redirect(reverse('lectureFinderApp:index'))


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('lectureFinderApp:members'))
            else:
                return render(request, 'lectureFinderApp/index.html', {'error_message': 'Account Deactivated'})
        else:
            return redirect(reverse('lectureFinderApp:index'))
    else:
        # When user tries to click MEMBERS link, but they aren't logged in.
        return redirect(reverse('lectureFinderApp:index'))


@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse('lectureFinderApp:index'))
