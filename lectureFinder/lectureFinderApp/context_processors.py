from .models import ThemeConfiguration

def theme(request):
    if request.user.is_authenticated:
        _theme = ThemeConfiguration.objects.filter(user=request.user).last()
    else:
        _theme = None
    return {
        'theme': _theme,
    }