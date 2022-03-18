from django import forms

class CourseForm(forms.Form):
	class Meta:
        model = Course
        fields = ('name', 'code', 'user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.none()

        if 'name' in self.data:
            try:
                country_id = int(self.data.get('name'))
                self.fields['user'].queryset = User.objects.filter(name_id=name_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['user'].queryset = self.instance.country.user_set.order_by('name')