from django import forms
from .models import Post
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.forms import DateInput


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text_content', 'image', 'post_time', 'hour']

    post_time = forms.DateField(
        initial=datetime.now().date(),
        widget=DateInput(attrs={'type': 'date'})
    )

    hour = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        post_time = cleaned_data.get('post_time')
        hour = cleaned_data.get('hour')

        if post_time is not None and hour is not None:
            try:
             
                post_time = datetime.combine(post_time, datetime.min.time()) + timedelta(hours=hour)
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
