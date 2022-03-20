# from .models import ThemeConfiguration
from .forms import UserForm, UserProfileForm


# TODO: Do we really need the code below?
# def theme(request):
#     if request.user.is_authenticated:
#         _theme = ThemeConfiguration.objects.filter(user=request.user).last()
#     else:
#         _theme = None
#     return {
#         'theme': _theme,
#     }


def signup_form(request):
    return {
        'user_form': UserForm(),
        'user_profile_form': UserProfileForm()
    }
