from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # User model by default provides user_id, username, first & surname, email, password.
    is_professor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.TextField(max_length=128, unique=False)
    code = models.IntegerField(unique=True, default=0)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    title = models.TextField(max_length=128, unique=True)
    video_url = models.URLField(max_length=400)
    slideshow_url = models.URLField(max_length=400)
    transcript_name = models.TextField(max_length=128, default="")
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    # Default of None only helps in the case of migrating an empty DB -- the .save() method
    # means this slug will always be populated.
    slug = models.SlugField(unique=True, default=None)

    # Foreign keys (which course & professor is this lecture linked to?)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Lecture, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title) + " => for " + str(self.course)


class SavedLecture(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.lecture) + ", saved by, " + str(self.user)

