from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Lecture, SavedLecture, UserProfile, Course, LikedLecture
from .forms import UserForm, UserProfileForm, UploadLectureForm
from .extract_questions import search_transcripts_for_phrase


class LikeLectureView(View):
    @method_decorator(login_required)
    def get(self, request):
        lecture_id = request.GET['lecture_id']

        try:
            lecture = Lecture.objects.get(id=int(lecture_id))
        except Lecture.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        current_user = UserProfile.objects.get(user=User.objects.get(id=request.user.id))
        liked_lecture, liked_lecture_was_created = LikedLecture.objects.get_or_create(user=current_user, lecture=lecture)

        if liked_lecture_was_created:
            lecture.likes += 1
            lecture.save()

        return HttpResponse(lecture.likes)


def index(request):
    # Index page will display both the 10 most recently uploaded and the 10 most viewed lectures.
    all_lectures = Lecture.objects.all()  # ordered by last record inserted into the table.
    all_lectures_by_views = all_lectures.order_by('-views')

    context_dict = {
        'recently_uploaded': all_lectures[:10],
        'most_viewed': all_lectures_by_views[:10],
    }

    return render(request, 'lectureFinderApp/index.html', context=context_dict)


def about(request):
    return render(request, 'lectureFinderApp/about.html')


def terms_and_conditions(request):
    return render(request, 'lectureFinderApp/terms_and_conditions.html')


@login_required
def members(request):
    if request.method == 'POST':
        upload_lecture_form = UploadLectureForm(request.POST)

        if upload_lecture_form.is_valid():
            new_lecture = upload_lecture_form.save(commit=False)
            new_lecture.course = Course.objects.get(code=request.POST.get('course'))
            new_lecture.professor = UserProfile.objects.get(user=User.objects.get(id=request.user.id))
            new_lecture.save()

            return redirect(reverse('lectureFinderApp:members'))
        else:
            messages.add_message(request, messages.ERROR, message=upload_lecture_form.errors)
            return redirect(reverse('lectureFinderApp:members'))

    else:
        upload_lecture_form = UploadLectureForm()

        logged_in_user = User.objects.get(id=request.user.id)
        logged_in_user = UserProfile.objects.get(user=logged_in_user)
        all_saved_lectures_for_user = SavedLecture.objects.all().filter(user=logged_in_user)

        context_dict = {
            'saved_lectures': all_saved_lectures_for_user,
            'user_profile': logged_in_user,
            'upload_lecture_form': upload_lecture_form,
            'courses': Course.objects.all(),
            'professors': UserProfile.objects.all().filter(is_professor=True)
        }

        return render(request, 'lectureFinderApp/members.html', context=context_dict)


def search(request):
    all_lectures = Lecture.objects.all()

    context_dict = {
        'courses': Course.objects.all(),
        'professors': UserProfile.objects.all().filter(is_professor=True),
        'range': range(1, 11),
        'search_results': all_lectures
    }

    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        refined_course_code = int(request.POST.get('refine_course'))
        refined_lecturer_id = int(request.POST.get('refine_lecturer'))
        refined_week = int(request.POST.get('refine_week'))
        search_results = search_transcripts_for_phrase(search_query)

        returned_lectures_by_query = []
        for lecture in all_lectures:
            if len(search_query) == 0:
                returned_lectures_by_query.append(lecture)
            else:
                for result in search_results:
                    if lecture.transcript_name == result:
                        returned_lectures_by_query.append(lecture)

        returned_lectures = returned_lectures_by_query.copy()
        for lecture in returned_lectures_by_query:
            if refined_course_code != -1 and lecture.course.code != refined_course_code:
                returned_lectures.remove(lecture)

            elif refined_lecturer_id != -1 and lecture.professor.user.id != refined_lecturer_id:
                returned_lectures.remove(lecture)

            elif refined_week != -1 and lecture.week != refined_week:
                returned_lectures.remove(lecture)

        context_dict['search_results'] = returned_lectures

    return render(request, 'lectureFinderApp/search.html', context=context_dict)


def show_lecture(request, lecture_name_slug):
    context_dict = {}
    lecture_to_show = Lecture.objects.get(slug=lecture_name_slug)

    # Increment view count on this lecture, while we are here.
    lecture_to_show.views += 1
    lecture_to_show.save()

    context_dict['lecture'] = lecture_to_show

    # Get the saved lectures for this user, so we know if this lecture has been saved or not already!
    try:
        current_user = UserProfile.objects.get(user=User.objects.get(id=request.user.id))
        saved_lecture = get_saved_lectures(lecture_name_slug, current_user)
    except (UserProfile.DoesNotExist, User.DoesNotExist, Lecture.DoesNotExist, SavedLecture.DoesNotExist):
        saved_lecture = None
    context_dict['saved_lecture'] = saved_lecture

    try:
        user_has_liked_lecture = LikedLecture.objects.get(user=current_user, lecture=lecture_to_show)
    except LikedLecture.DoesNotExist:
        user_has_liked_lecture = None
    context_dict['user_has_liked_lecture'] = user_has_liked_lecture

    return render(request, 'lectureFinderApp/show_lecture.html', context=context_dict)


@login_required
def save_lecture(request, lecture_name_slug):
    current_user = UserProfile.objects.get(user=User.objects.get(id=request.user.id))

    saved_lecture = SavedLecture.objects.create(
        lecture=Lecture.objects.get(slug=lecture_name_slug),
        user=current_user
    )
    saved_lecture.save()

    return redirect(reverse('lectureFinderApp:members'))


@login_required
def delete_saved_lecture(request, lecture_name_slug):
    current_user = UserProfile.objects.get(user=User.objects.get(id=request.user.id))
    get_saved_lectures(lecture_name_slug, current_user).delete()

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

            messages.add_message(request, messages.SUCCESS, "Signed up! Please login now.")
            return redirect(reverse('lectureFinderApp:index'))
        else:
            error_string = str(user_form.errors) + str(user_profile_form.errors)
            messages.add_message(request, messages.ERROR, error_string)
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
                messages.add_message(request, messages.ERROR, "Your account has been disabled.")
                return redirect(reverse('lectureFinderApp:index'))
        else:
            messages.add_message(request, messages.ERROR, "Invalid login details.")
            return redirect(reverse('lectureFinderApp:index'))
    else:
        # When user tries to go to the MEMBERS link, but they aren't logged in.
        messages.add_message(request, messages.ERROR, "You must be logged in to access the members area.")
        return redirect(reverse('lectureFinderApp:index'))


@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse('lectureFinderApp:index'))


# Helper functions
def get_saved_lectures(lecture_name_slug, current_user):
    return SavedLecture.objects.get(
        lecture=Lecture.objects.get(slug=lecture_name_slug),
        user=current_user
    )
