from django import forms
from .models import Post
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.forms import DateInput


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text_content', 'image', 'post_time', 'hour']
        labels = {
            'title': '제목',
            'image': '이미지',
        }

    text_content = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 30, 'rows': 1}),
        )    

    post_time = forms.DateField(
        initial=datetime.now().date(),
        widget=DateInput(attrs={'type': 'date'}),
        label='날짜',
    )
    # 시간 선택 범위 설정
    HOUR_CHOICES = [(str(hour), str(hour)) for hour in range(24)]
    
    hour = forms.ChoiceField(choices=HOUR_CHOICES, label='시간')

    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'accept':'image/*'}),
    )
    
    def clean(self):
        cleaned_data = super().clean()
        post_time = cleaned_data.get('post_time')
        hour = cleaned_data.get('hour')

        if post_time is not None and hour is not None:
            try:
             
                post_time = datetime.combine(post_time, datetime.min.time()) + timedelta(hours=int(hour))
            except ValueError:
                raise forms.ValidationError('Invalid date or time')

            cleaned_data['post_time'] = post_time


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text_content', 'post_time', 'hour']

    title = forms.CharField(required=True)
    text_content = forms.CharField(required=True)
    post_time = forms.DateTimeField(required=True)
    hour = forms.IntegerField(required=True)



class DateRangeFilterForm(forms.Form):
    start_date = forms.DateField(
        label='시작 날짜',
        required=False,
        widget=forms.TextInput(attrs={'type': 'date', 'value': now().date(), 'class': 'custom-date-input'})
    )
    end_date = forms.DateField(
        label='마지막 날짜',
        required=False,
        widget=forms.TextInput(attrs={'type': 'date', 'value': now().date(), 'class': 'custom-date-input'})
    )
