from django import forms
from .models import Post
from django.utils.timezone import now
from datetime import datetime

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text_content', 'image', 'year', 'month', 'day', 'hour',]

    year = forms.IntegerField(initial=datetime.now().year)
    month = forms.IntegerField(initial=datetime.now().month)
    day = forms.IntegerField(initial=datetime.now().day)
    hour = forms.IntegerField(initial=datetime.now().hour)

    def clean(self):
        cleaned_data = super().clean()
        year = cleaned_data.get('year')
        month = cleaned_data.get('month')
        day = cleaned_data.get('day')
        hour = cleaned_data.get('hour')

        if year is not None and month is not None and day is not None and hour is not None:
            try:
                post_time = datetime(year, month, day, hour)
            except ValueError:
                raise forms.ValidationError('Invalid date or time')

            cleaned_data['post_time'] = post_time


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image']

    title = forms.CharField(required=True)  # 선택적으로 제목 수정 가능하도록
    image = forms.ImageField(required=True)  # 선택적으로 이미지 수정 가능하도록


class DateRangeFilterForm(forms.Form):
    start_date = forms.DateField(
        label='Start Date',
        required=False,
        widget=forms.TextInput(attrs={'type': 'date', 'value': now().date()})
    )
    end_date = forms.DateField(
        label='End Date',
        required=False,
        widget=forms.TextInput(attrs={'type': 'date', 'value': now().date()})
    )
