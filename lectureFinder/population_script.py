import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lectureFinder.settings')

import django

django.setup()
from lectureFinderApp.models import UserProfile, Course, Lecture, SavedLecture
from django.contrib.auth.models import User


def populate():
    courses = [
        {'name': 'WAD2', 'code': 2021},
        {'name': 'OOSE2', 'code': 2008},
        {'name': 'ADS2', 'code': 2007},
        {'name': 'AF2', 'code': 2003},
        {'name': 'NOSE2', 'code': 2024},
        {'name': 'JP2', 'code': 2001},
    ]

    users = [
        {'first_name': 'Derek', 'last_name': 'Somerville', 'email': 'email1@gmail.com', 'is_professor': True},
        {'first_name': 'Alistair', 'last_name': 'Morrison', 'email': 'email2@gmail.net', 'is_professor': True},
        {'first_name': 'Michele', 'last_name': 'Sevegnani', 'email': 'email3@gmail.net', 'is_professor': True},
        {'first_name': 'Gethin', 'last_name': 'Norman', 'email': 'email4@gmail.net', 'is_professor': True},
        {'first_name': 'Mary Ellen', 'last_name': 'Foster', 'email': 'email5@gmail.net', 'is_professor': True},
        {'first_name': 'Angelos', 'last_name': 'Marnerides', 'email': 'email6@gmail.net', 'is_professor': True},
        {'first_name': 'Luke', 'last_name': 'Mullen', 'email': 'email4@gmail.net'},
        {'first_name': 'John', 'last_name': 'Smith', 'email': 'email5@gmail.net'},
        {'first_name': 'David', 'last_name': 'Black', 'email': 'email6@gmail.net'},
    ]

    for course in courses:
        add_course(**course)

    professors, students = [], []
    for user in users:
        person = add_user(**user)
        if user.get('is_professor'):
            professors.append(person)
        else:
            students.append(person)

    # Dictionary of (unique) course codes to a list of lecture objects.
    lectures = {
        2021: [
            {
                'title': 'Lecture 1-A',
                'transcript_name': '',
                'video_url': 'https://moodle.gla.ac.uk/mod/lti/view.php?id=2774846',
                'slideshow_url': 'https://moodle.gla.ac.uk/pluginfile.php/5180587/mod_resource/content/1/L1-Introduction-notes.pdf',
                'professor': professors[1],
                'views': 35,
                'week': 1
            }
        ],
        2008: [
            {
                'title': '5.1 Monday Lecture - Mocking',
                'transcript_name': 'OOSE2_mocking_transcript.vtt',
                'video_url': 'https://uofglasgow.zoom.us/rec/play/Gnh6zBh2sxyjQgqY7Zb-zRm4CpjIWHtigZtPwfalth-JYCHDVcDaXc4zREq8eX7AqK9-CAUIhVTAGc7T.aDtc97nEaL726nun?startTime=1644231182000&_x_zm_rtaid=Kn8QJRdNTW2kousYc7ITPQ.1647047085571.d7a9e03007c63ee4c99d3454883e0232&_x_zm_rhtaid=206',
                'slideshow_url': 'https://gla.sharepoint.com/:p:/r/sites/COMPSCI2008OBJECT-ORIENTEDSOFTWAREENGINEERING22/_layouts/15/Doc.aspx?sourcedoc=%7BF25477F5-9A3F-4636-9D46-AF69742A1790%7D&file=OOSE%205.1.2%20Doubling%20and%20Mocking.pptx&action=edit&mobileredirect=true',
                'professor': professors[0],
                'views': 44,
                'week': 5
            }
        ],
        2007: [
            {
                'title': 'Lecture 4 - Recursive Algorithms',
                'transcript_name': 'ADS2_recursive_algorithms_transcript.vtt',
                'video_url': 'https://uofglasgow.zoom.us/rec/play/JpbFui0-YvvulfNUERinFS-sHu9y9aUs3wDwGUU9gg97mzJUeFlZhf5cnCx2EYsJ4DVywo1TDUXDX9rS.rSFtpaMpwET_hUII?continueMode=true&_x_zm_rtaid=M70fcYTzQIibJD29XdCmug.1647531154126.915d917426e55bec361cfc35e932e89e&_x_zm_rhtaid=698',
                'slideshow_url': 'https://moodle.gla.ac.uk/pluginfile.php/4813403/mod_folder/content/0/L4.pptx?forcedownload=1',
                'professor': professors[2],
                'views': 68,
                'week': 2
            },

            {
                'title': 'ADS2 - Lecture 5 - MERGE SORT',
                'transcript_name': 'ADS2_merge_sort_transcript.vtt',
                'video_url': 'https://uofglasgow.zoom.us/rec/play/l5_NrzmZizGtIEU14tw48_Hsmk0lWCRAmMnys1n7dxYa8X3mDNcmAQA4s55ZMbnQvvrdFUGaLc0tYEeN.06DWBCPf86ox6iof?continueMode=true&_x_zm_rtaid=Eec8LpnvRpKOq198-1c_mw.1648433865556.223cbaf9613b52610ba63ef83260fb6a&_x_zm_rhtaid=980',
                'slideshow_url': 'https://moodle.gla.ac.uk/pluginfile.php/4813403/mod_folder/content/0/L5.pptx?forcedownload=1',
                'professor': professors[2],
                'views': 103,
                'week': 1
            }
        ],
        2024: [
            {
                'title': 'Topic 8 - TLS',
                'transcript_name': '',
                'video_url': 'https://uofglasgow.zoom.us/rec/play/x2LkSCG96eCY7VNopDTOsyEttrjed46OdszGVBYm7SSNGyvad49SCyKzIIo5AqygP3CVzfScr9DMg6Fl.Ol_IZqhIAlt4yBzi?startTime=1603134412000&_x_zm_rtaid=Eec8LpnvRpKOq198-1c_mw.1648433865556.223cbaf9613b52610ba63ef83260fb6a&_x_zm_rhtaid=980',
                'slideshow_url': 'https://moodle.gla.ac.uk/pluginfile.php/4812897/mod_resource/content/1/Security%20and%20Privacy_1.pdf',
                'professor': professors[5],
                'views': 33,
                'week': 4
            }
        ],
        2001: [
            {
                'title': 'JP2 Week 1 Lecture Video',
                'transcript_name': '',
                'video_url': 'https://web.microsoftstream.com/video/d506f755-a79a-4393-90b8-33d94d321df3?referrer=https:%2F%2Fmoodle.gla.ac.uk%2F',
                'slideshow_url': 'https://moodle.gla.ac.uk/pluginfile.php/4810872/mod_resource/content/1/2021-09-27.pdf',
                'professor': professors[4],
                'views': 83,
                'week': 1
            }
        ],
        2003: [
            {
                'title': 'Lecture 6 (Numbers - Part 1) - Video 2',
                'transcript_name': '',
                'video_url': 'https://uofglasgow.zoom.us/rec/play/Q_jMuxRWON93DbJ1EBNSR3-DWHlERyMe5-4U2hcTG7IUpPMEztkGfvHs1xSvWon38ixmOvRophQezYTq.ytrrF2vmtUaZYbBC?startTime=1599730606000&_x_zm_rtaid=Eec8LpnvRpKOq198-1c_mw.1648433865556.223cbaf9613b52610ba63ef83260fb6a&_x_zm_rhtaid=980',
                'slideshow_url': 'https://moodle.gla.ac.uk/pluginfile.php/4810872/mod_resource/content/1/2021-09-27.pdf',
                'professor': professors[3],
                'views': 83,
                'week': 1
            }
        ]
    }

    save_lectures = []
    for course_code, lectures in lectures.items():
        course = Course.objects.get(code=course_code)
        for lecture in lectures:
            save_lectures.append(add_lecture(
                course=course,
                professor=lecture.get('professor'),
                title=lecture.get('title'),
                video_url=lecture.get('video_url'),
                slideshow_url=lecture.get('slideshow_url'),
                transcript_name=lecture.get('transcript_name'),
                views=lecture.get('views'),
                week=lecture.get('week')
            ))

    saved_lectures = [
        {'user': students[0], 'lecture': save_lectures[1]},
        {'user': students[0], 'lecture': save_lectures[2]},
        {'user': students[1], 'lecture': save_lectures[0]},
    ]

    for save in saved_lectures:
        save_a_lecture(**save)


def add_course(name, code):
    c = Course.objects.get_or_create(name=name, code=code)[0]
    c.save()
    return c


def add_lecture(title, video_url, transcript_name, slideshow_url, course, professor, week, views=0, likes=0):
    l = Lecture.objects.get_or_create(title=title, course=course, professor=professor)[0]
    l.video_url = video_url
    l.slideshow_url = slideshow_url
    l.transcript_name = transcript_name
    l.views = views
    l.likes = likes
    l.week = week
    l.save()
    return l


def add_user(first_name, last_name, email, is_professor=False):
    # first create a user record using django's user model
    django_user = \
        User.objects.get_or_create(username=first_name + last_name, first_name=first_name, last_name=last_name,
                                   email=email)[0]
    django_user.save()

    user = UserProfile.objects.get_or_create(user=django_user, is_professor=is_professor)[0]
    user.save()
    return user


def save_a_lecture(lecture, user):
    saved_lecture = SavedLecture.objects.get_or_create(lecture=lecture, user=user)[0]
    saved_lecture.save()
    return saved_lecture


if __name__ == "__main__":
    print('Starting population script...')
    populate()
