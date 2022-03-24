from django.test import TestCase
from django.contrib.auth.models import User
from lectureFinderApp.models import Lecture, Course, UserProfile
from django.urls import reverse


# Create your tests here.
class LectureMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        Ensure that this lecture has at least 0 views.
        """
        lecturer = create_mock_lecturer()
        course = create_mock_course()
        lecture = create_mock_lecture(
            title="OOSE2 Mocking Lecture 5.1",
            video_url="site.com",
            slideshow_url="site2.com",
            transcript_name="Lecture1.vtt",
            views=-4,
            likes=15,
            week=0,
            course=course,
            professor=lecturer
        )
        lecture.save()

        self.assertEqual((lecture.views >= 0), True)

    def test_ensure_likes_are_positive(self):
        """
        Ensure that this lecture has at least 0 likes.
        """
        lecturer = create_mock_lecturer()
        course = create_mock_course()
        lecture = create_mock_lecture(
            title="OOSE2 Mocking Lecture 5.1",
            video_url="site.com",
            slideshow_url="site2.com",
            transcript_name="Lecture1.vtt",
            views=4,
            likes=-15,
            week=0,
            course=course,
            professor=lecturer
        )

        self.assertEqual((lecture.likes >= 0), True)

    def test_ensure_week_is_positive(self):
        """
        Ensure that this lecture was uploaded on a week greater than week 0.
        """
        lecturer = create_mock_lecturer()
        course = create_mock_course()
        lecture = create_mock_lecture(
            title="OOSE2 Mocking Lecture 5.1",
            video_url="site.com",
            slideshow_url="site2.com",
            transcript_name="Lecture1.vtt",
            views=4,
            likes=15,
            week=0,
            course=course,
            professor=lecturer
        )

        self.assertEqual((lecture.week > 0), True)

    def test_slug_line_creation(self):
        """
        Checks to see if the created slug for this lecture is correct
        e.g if the title is "OOSE2 Mocking Lecture 5.1", the slug should be
        "oose2-mocking-lecture-51"
        """
        lecturer = create_mock_lecturer()
        course = create_mock_course()
        lecture = create_mock_lecture(
            title="OOSE2 Mocking Lecture 5.1",
            video_url="site.com",
            slideshow_url="site2.com",
            transcript_name="Lecture1.vtt",
            views=4,
            likes=15,
            week=0,
            course=course,
            professor=lecturer
        )

        self.assertEqual(lecture.slug, 'oose2-mocking-lecture-51')


class IndexViewTests(TestCase):
    def test_index_view_with_no_lectures(self):
        """
        If there are no lectures, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('lectureFinderApp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recent lectures.')
        self.assertQuerysetEqual(response.context['most_viewed'], [])
        self.assertQuerysetEqual(response.context['recently_uploaded'], [])

    def test_index_view_with_lectures(self):
        """
        Checks whether lectures are displayed correctly when they are present.
        """
        lecturer = create_mock_lecturer()
        course = create_mock_course()

        create_mock_lecture(
            title="OOSE2 Mocking Lecture 5.1",
            video_url="site.com",
            slideshow_url="site2.com",
            transcript_name="Lecture1.vtt",
            views=4,
            likes=15,
            week=0,
            course=course,
            professor=lecturer
        )

        create_mock_lecture(
            title="OOSE2 Faking Lecture 3.2",
            video_url="site2.com",
            slideshow_url="site23.com",
            transcript_name="Lecture3.vtt",
            views=8,
            likes=4,
            week=0,
            course=course,
            professor=lecturer
        )

        response = self.client.get(reverse('lectureFinderApp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'OOSE2 Mocking Lecture 5.1')
        self.assertContains(response, 'OOSE2 Faking Lecture 3.2')

        num_lectures = len(response.context['recently_uploaded'])
        self.assertEqual(num_lectures, 2)


class SearchViewTests(TestCase):
    def test_search_view_with_query(self):
        """
        Given a search query, ensure the correct result(s) is/are displayed.
        """
        lecturer = create_mock_lecturer()
        course = create_mock_course()

        create_mock_lecture(
            title="Lecture 4 - Recursive Algorithms",
            video_url="site.com",
            slideshow_url="site2.com",
            transcript_name="ADS2_recursive_algorithms_transcript.vtt",
            views=4,
            likes=15,
            week=0,
            course=course,
            professor=lecturer
        )

        response = self.client.get(reverse('lectureFinderApp:search'))
        self.assertEqual(response.status_code, 200)


def create_mock_lecturer():
    lecturer_user = User(
        username="JohnSmith13",
        first_name="John",
        last_name="Smith",
        email="johnsmith@gmail.com"
    )
    lecturer_user.save()

    lecturer = UserProfile(
        user=lecturer_user,
        is_professor=True
    )
    lecturer.save()
    return lecturer


def create_mock_course():
    course = Course(
        name="FakeCourse",
        code=4567
    )
    course.save()
    return course


def create_mock_lecture(**args):
    lecture = Lecture(**args)
    lecture.save()
    return lecture
